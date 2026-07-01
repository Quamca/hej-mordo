"""Rozpoznawanie twarzy Igora — InsightFace embeddings, podgląd w przeglądarce."""

import os
import queue
import threading
import time

import cv2
import numpy as np

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
_FACES_DIR = os.path.join(_BRAIN_DIR, "data", "faces", "igor")
_SIM_THRESHOLD = 0.35
_TIMEOUT_S = 3.0

_frame_q: queue.Queue = queue.Queue(maxsize=2)
_photo_requested = threading.Event()


def put_frame(data: bytes) -> None:
    if _frame_q.full():
        try:
            _frame_q.get_nowait()
        except queue.Empty:
            pass
    try:
        _frame_q.put_nowait(data)
    except queue.Full:
        pass


def request_photo() -> None:
    _photo_requested.set()


def _normed(embedding: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(embedding)
    return embedding / n if n > 0 else embedding


def _load_refs(app) -> list:
    refs = []
    if not os.path.isdir(_FACES_DIR):
        return refs
    for fname in sorted(os.listdir(_FACES_DIR)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        img = cv2.imread(os.path.join(_FACES_DIR, fname))
        if img is None:
            continue
        faces = app.get(img)
        if faces:
            refs.append(_normed(faces[0].embedding))
            print(f"[FACE] ref: {fname}")
    print(f"[FACE] referencji: {len(refs)}")
    return refs


def _igor_similarity(embedding: np.ndarray, refs: list) -> float:
    emb = _normed(embedding)
    return max((np.dot(emb, r) for r in refs), default=0.0)


def _send_state(state: str) -> None:
    from ws_server import enqueue_state
    enqueue_state(state)


def _send_face_box(payload: str) -> None:
    from ws_server import enqueue_face_box
    enqueue_face_box(payload)


def _trigger_gemini() -> None:
    from gemini_client import signal_igor_present
    signal_igor_present()


def _face_thread(loop) -> None:
    from insightface.app import FaceAnalysis

    print("[FACE] ładowanie modelu InsightFace (pierwsze uruchomienie pobiera ~100MB)...")
    app = FaceAnalysis(name="buffalo_sc", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(320, 320))
    print("[FACE] model gotowy")

    refs = _load_refs(app)

    igor_active = False
    last_igor_ts = 0.0
    frame_count = 0
    existing = [f for f in os.listdir(_FACES_DIR) if f.lower().endswith(".jpg")] if os.path.isdir(_FACES_DIR) else []
    photo_n = len(existing)

    print("[FACE] rozpoznawanie aktywne — zdjęcie referencyjne przez przycisk w przeglądarce")

    while True:
        try:
            data = _frame_q.get(timeout=0.5)
        except queue.Empty:
            if igor_active and time.time() - last_igor_ts > _TIMEOUT_S:
                igor_active = False
                loop.call_soon_threadsafe(_send_state, "listen")
            continue

        frame_count += 1
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            continue

        if _photo_requested.is_set():
            _photo_requested.clear()
            os.makedirs(_FACES_DIR, exist_ok=True)
            photo_n += 1
            path = os.path.join(_FACES_DIR, f"igor_{photo_n:04d}.jpg")
            cv2.imwrite(path, img)
            print(f"[FACE] zdjecie zapisane: {path}")
            refs = _load_refs(app)

        # InsightFace co 5. klatkę — detekcja + rozpoznawanie
        if frame_count % 5 == 0:
            h, w = img.shape[:2]
            faces = app.get(img)
            if not faces:
                loop.call_soon_threadsafe(_send_face_box, "none")
            for face in faces:
                sim = _igor_similarity(face.embedding, refs) if refs else 0.0
                igor = sim > _SIM_THRESHOLD
                label = "Igor" if igor else "?"
                x1, y1, x2, y2 = face.bbox.astype(int)
                nx1, ny1, nx2, ny2 = x1 / w, y1 / h, x2 / w, y2 / h
                loop.call_soon_threadsafe(
                    _send_face_box, f"{nx1:.3f},{ny1:.3f},{nx2:.3f},{ny2:.3f},{label}"
                )
                if igor:
                    last_igor_ts = time.time()
                    if not igor_active:
                        igor_active = True
                        print(f"[FACE] Igor rozpoznany ({sim:.2f})")
                        loop.call_soon_threadsafe(_send_state, "face")
                        loop.call_soon_threadsafe(_trigger_gemini)

        # Timeout — twarz zniknęła >3s
        if igor_active and time.time() - last_igor_ts > _TIMEOUT_S:
            igor_active = False
            loop.call_soon_threadsafe(_send_state, "listen")


def start(loop) -> None:
    os.makedirs(_FACES_DIR, exist_ok=True)
    threading.Thread(target=_face_thread, args=(loop,), daemon=True).start()

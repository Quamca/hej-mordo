"""Rozpoznawanie twarzy Igora — InsightFace embeddings + cv2 preview."""

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


def _is_igor(embedding: np.ndarray, refs: list) -> bool:
    emb = _normed(embedding)
    return any(np.dot(emb, r) > _SIM_THRESHOLD for r in refs)


def _send_state(state: str) -> None:
    from ws_server import enqueue_state
    enqueue_state(state)


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

    print("[FACE] podgląd aktywny — 'd' = zrób zdjęcie referencyjne")

    while True:
        try:
            data = _frame_q.get(timeout=0.5)
        except queue.Empty:
            if igor_active and time.time() - last_igor_ts > _TIMEOUT_S:
                igor_active = False
                loop.call_soon_threadsafe(_send_state, "listen")
            cv2.waitKey(1)
            continue

        frame_count += 1
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            continue

        # InsightFace co 5. klatkę — detekcja + rozpoznawanie
        if frame_count % 5 == 0:
            faces = app.get(img)
            for face in faces:
                igor = refs and _is_igor(face.embedding, refs)
                color = (0, 200, 0) if igor else (0, 0, 200)
                x1, y1, x2, y2 = face.bbox.astype(int)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                label = "Igor" if igor else "?"
                cv2.putText(img, label, (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                if igor:
                    last_igor_ts = time.time()
                    if not igor_active:
                        igor_active = True
                        loop.call_soon_threadsafe(_send_state, "face")

        # Timeout — twarz zniknęła >3s
        if igor_active and time.time() - last_igor_ts > _TIMEOUT_S:
            igor_active = False
            loop.call_soon_threadsafe(_send_state, "listen")

        cv2.imshow("Mordo — kamera", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("d"):
            os.makedirs(_FACES_DIR, exist_ok=True)
            photo_n += 1
            path = os.path.join(_FACES_DIR, f"igor_{photo_n:04d}.jpg")
            cv2.imwrite(path, img)
            print(f"[FACE] zdjecie zapisane: {path}")
            refs = _load_refs(app)


def start(loop) -> None:
    os.makedirs(_FACES_DIR, exist_ok=True)
    threading.Thread(target=_face_thread, args=(loop,), daemon=True).start()

---
title: "ISSUE-020: Kamera laptopa — face recognition + zdjęcie referencyjne"
status: done
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Mordo widzi przez kamerę laptopa i rozpoznaje Igora. Z poziomu przeglądarki można zrobić zdjęcie referencyjne.

## Podejście (zmienione względem pierwotnego planu)

Pierwotny plan zakładał `pc_mordo.py` + OpenCV `VideoCapture(0)` — ten plik już nie istnieje po pivocie
z ISSUE-019 na architekturę przeglądarkową. Kamera laptopa idzie tą samą drogą co mikrofon:
`pc_mordo.html` (`getUserMedia video`) → WebSocket (nagłówek `CAM\x00`, jak ESP32) → `ws_server.py`
→ `frame_callbacks` → `face.py`. Zero zmian w `ws_server.py` dla samej dystrybucji klatek.

Podgląd z ramką wokół twarzy przeniesiony z osobnego okna cv2 do przeglądarki — `face.py` wysyła tylko
współrzędne ramki (znormalizowane 0..1) i etykietę przez WebSocket (`FACE:x1,y1,x2,y2,label`),
przeglądarka rysuje nakładkę na własnym, już wyświetlanym obrazie z kamery.

## Acceptance Criteria

- [x] Klatki z kamery laptopa trafiają do `face.py` (przez przeglądarkę + `ws_server.py`, nie OpenCV bezpośrednio)
- [x] Face recognition działa na klatkach z laptopa (ten sam InsightFace co ISSUE-015)
- [x] Przycisk "Zrób zdjęcie referencyjne" w przeglądarce → zapisuje do `brain/data/faces/igor/`
- [x] Po zapisaniu zdjęcia — system od razu je ładuje (bez restartu)
- [x] Rozpoznanie Igora loguje się w terminalu: `[FACE] Igor rozpoznany (0.XX)`

## Notatki

- `pc_mordo.html`: `getUserMedia({video:true})` + `<canvas>` → JPEG (5fps) → WebSocket binary z nagłówkiem `CAM\x00`
- `ws_server.py`: dodano `photo_callbacks` (analogicznie do `frame_callbacks`) i obsługę tekstowej komendy `"PHOTO"` od klienta; dodano `enqueue_face_box()`
- `face.py`: usunięto `cv2.imshow`/`waitKey` (osobne okno) — zastąpione wysyłaniem `FACE:` przez WebSocket; `request_photo()` (threading.Event) zastępuje klawisz `d`
- `main.py`: rejestruje `photo_callbacks.append(face.request_photo)`
- Zdjęcie referencyjne: `brain/data/faces/igor/igor_NNNN.jpg` (auto-numeracja) — bez zmian względem ISSUE-015
- Zależność: ISSUE-019 done

## Test manualny

1. `cd brain && python main.py`
2. Otwórz `pc_mordo.html`, kliknij "Połącz z Mordo", zezwól na kamerę
3. Ramka i etykieta "Igor"/"?" pojawiają się na podglądzie kamery w przeglądarce
4. Kliknij "Zrób zdjęcie referencyjne" → nowy plik `igor_NNNN.jpg` w `brain/data/faces/igor/`, log `[FACE] zdjecie zapisane`
5. Odejdź i wróć przed kamerę → terminal loguje `[FACE] Igor rozpoznany (0.XX)`

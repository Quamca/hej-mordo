---
title: "ISSUE-020: Kamera laptopa — face recognition + zdjęcie referencyjne"
status: planned
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Mordo widzi przez kamerę laptopa i rozpoznaje Igora. Z poziomu programu można zrobić zdjęcie referencyjne (bez zewnętrznych narzędzi).

## Acceptance Criteria

- [ ] `pc_mordo.py` czyta klatki z kamery laptopa (OpenCV `VideoCapture(0)`)
- [ ] Face recognition działa na klatkach z laptopa (ten sam InsightFace co ISSUE-015)
- [ ] Komenda w terminalu `foto` → robi zdjęcie referencyjne i zapisuje do `brain/data/faces/igor/`
- [ ] Po zapisaniu zdjęcia — system od razu je ładuje (bez restartu)
- [ ] Rozpoznanie Igora loguje się w terminalu: `[FACE] Igor rozpoznany (0.87)`

## Notatki

- Nowy moduł: `brain/cam_local.py` — OpenCV capture w osobnym wątku, dostarcza klatki JPEG
- `face.py` zostaje bez zmian — przyjmuje bytes JPEG tak samo jak z ESP32
- Komenda `foto` wpisywana w terminalu (stdin) podczas działania programu
- Zdjęcie referencyjne: `brain/data/faces/igor/igor_NNNN.jpg` (auto-numeracja)
- Zależność: ISSUE-019 done

## Test manualny

1. `python pc_mordo.py` → w terminalu wpisz `foto` → stań przed kamerą
2. Plik `igor_NNNN.jpg` pojawia się w `brain/data/faces/igor/`
3. Odejdź i wróć przed kamerę → terminal loguje rozpoznanie

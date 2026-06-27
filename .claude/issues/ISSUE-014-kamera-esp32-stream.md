---
title: "ISSUE-014: Kamera ESP32 — inicjalizacja i stream JPEG do brain"
status: planned
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-27
updated: 2026-06-27
---

## Cel

ESP32 inicjalizuje kamerę OV3660 i strumieniuje klatki JPEG do brain przez WebSocket — brain może je odbierać i przetwarzać.

## Acceptance Criteria

- [ ] Kamera OV3660 inicjalizuje się poprawnie (brak błędów w Serial)
- [ ] ESP32 wysyła klatki JPEG przez WebSocket do brain (osobny typ wiadomości np. prefix `CAM:` lub osobny kanał)
- [ ] Brain odbiera klatki i loguje że je dostał (np. "frame received, size=NNN bytes")
- [ ] Częstotliwość: ~5 fps (wystarczy do rozpoznawania twarzy, nie przeciąża WiFi)

## Notatki

- XIAO ESP32-S3 Sense ma wbudowany slot kamery (FPC) — OV3660 podpięty przez taśmę 75mm
- Kamera przez `esp_camera.h` (esp32-camera library)
- Rozdzielczość: QVGA (320×240) lub CIF (352×288) — wystarczy do twarzy, mniejszy payload
- Uwaga: kamera i mikrofon PDM mogą konkurować o zasoby DMA — sprawdzić czy działają jednocześnie
- Zależność: ISSUE-015 czeka na ten issue

## Test manualny

1. Uruchom brain (main.py) i wgraj firmware
2. W logach brain: widać "frame received" co ~200ms
3. Opcjonalnie: brain zapisuje jedną klatkę jako plik .jpg i Igor ją sprawdza

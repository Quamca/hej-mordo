# Mordo — Stan Projektu

## Aktualna faza
Faza 0 — Software Mordo (laptop) — EPIC-1 w toku

## Co jest zrobione
- Struktura projektu i agenci Claude Code
- ISSUE-006: Mikrofon ESP32-S3 Sense — firmware PDM działa
- ISSUE-007: Jakość mikrofonu — 16kHz, 16-bit, jakość dobra
- ISSUE-008: WiFi + WebSocket — ESP32 strumieniuje audio PCM do brain
- ISSUE-009: Pełna pętla audio — ESP32 mic → brain → Gemini → głośnik PC, multi-turn działa
- ISSUE-010: Streaming playback + barge-in + VAD 400ms/200ms — działa
- ISSUE-012: Ekran LCD Round Display — GC9A01 + LovyanGFX, stany IDLE/LISTEN/SPEAK wyświetlane poprawnie
- ISSUE-013: Menu swipe — widok WiFi z siłą sygnału (RSSI kreski) i SSID. Interrupt-driven (CHSC6X FALLING edge).
- ISSUE-014: Kamera ESP32 OV3660 — stream JPEG ~5fps do brain przez WebSocket (CAM\0 header).
- ISSUE-015: Rozpoznawanie twarzy Igora (InsightFace buffalo_sc) — ekran "siema" na zielonym tle.
- ISSUE-016: Widok kamery na LCD — carousel WIFI←MAIN→CAMERA swipe, obraz 5fps na ekranie.

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Co teraz
ISSUE-019 done — PC audio przez przeglądarkę (`brain/pc_mordo.html` + istniejący `main.py`/`ws_server.py`).
Mikrofon, głośnik, barge-in i czyste zamknięcie (Ctrl+C) potwierdzone. Natywne audio (sounddevice+tkinter)
porzucone — twardy crash Windows przy mikrofon+głośnik+GUI jednocześnie (szczegóły w ISSUE-019 → Problemy
i rozwiązania). Next: ISSUE-020 (kamera laptopa + face recognition).

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-07-01 — ISSUE-019: natywne audio (sounddevice+tkinter) crashowało twardo (Windows 0xc0000005),
izolacja przez eliminację, przejście na przeglądarkę + istniejący ws_server.py. Mikrofon/głośnik/barge-in
potwierdzone działające.

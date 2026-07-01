# Mordo — Stan Projektu

## Aktualna faza
Faza 0 — Software Mordo (laptop) — EPIC-1 done

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
- ISSUE-019: PC audio przez przeglądarkę (`pc_mordo.html`) — mikrofon, głośnik, barge-in, Ctrl+C czysty.
- ISSUE-020: Kamera laptopa w przeglądarce — rozpoznawanie twarzy (ramka+etykieta), zdjęcie referencyjne.
- ISSUE-021: Auto-trigger — rozpoznanie Igora → powitanie Gemini → rozmowa lub dismiss (30s cooldown).

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Co teraz
EPIC-1 (Software Mordo Faza 0) zamknięty — ISSUE-019, 020, 021 wszystkie done. `pc_mordo.html` to
pełny interfejs Mordo na laptopie: mikrofon, głośnik, barge-in, kamera z rozpoznawaniem twarzy,
zdjęcie referencyjne, auto-trigger powitania przy rozpoznaniu Igora z dismissem (function call
`zakoncz_rozmowe`) i 30s cooldownem. Backend (`main.py`/`ws_server.py`/`face.py`/`gemini_client.py`)
niezmieniony względem architektury ESP32 — przeglądarka to po prostu kolejny klient WebSocket.
Natywne audio (sounddevice+tkinter) porzucone — twardy crash Windows przy mikrofon+głośnik+GUI
jednocześnie (szczegóły w ISSUE-019 → Problemy i rozwiązania).
`brain/main.py` teraz dubluje logi do `brain/mordo.log` (nadpisywany co start).

Next: EPIC-2 (Hardware Mordo Faza 1) — zostały ISSUE-011 (głośnik ESP32, czeka na lutowanie) i
ISSUE-018 (Gemini trigger przy rozpoznaniu twarzy na ESP32). Ewentualnie ISSUE-003 (wake word "Hej
Mordo") jeśli Igor zechce dodać wywoływanie głosem do auto-triggera z ISSUE-021.

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-07-01 — EPIC-1 zamknięty. ISSUE-019: natywne audio (sounddevice+tkinter) crashowało twardo
(Windows 0xc0000005), przejście na przeglądarkę + istniejący ws_server.py. ISSUE-020: kamera laptopa
w przeglądarce, rozpoznawanie twarzy bez osobnego okna cv2. ISSUE-021: auto-trigger powitania +
dismiss przez function-call Gemini — po drodze bug (zgubiona pętla `while True` w `_receive_audio`
powodowała zapętlone powitania), znaleziony przez logi per-tura.

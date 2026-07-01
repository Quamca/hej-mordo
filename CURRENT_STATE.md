# Mordo — Stan Projektu

## Aktualna faza
Faza 0 done (EPIC-1) — w trakcie EPIC-3 (Faza 2 "Pamięć", świadomie przed Fazą 1 hardware)

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
- ISSUE-003: Wake word "Hej Mordo" — Vosk offline (PL), aktywacja głosowa pomija cooldown dismissu.
- ISSUE-022: Google OAuth (Drive API) — `gdrive_auth.py`, token odświeżany automatycznie bez re-loginu.

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Co teraz
EPIC-1 (Software Mordo Faza 0) zamknięty — ISSUE-019, 020, 021, 003 wszystkie done. `pc_mordo.html` to
pełny interfejs Mordo na laptopie: mikrofon, głośnik, barge-in, kamera z rozpoznawaniem twarzy,
zdjęcie referencyjne, auto-trigger powitania (rozpoznanie twarzy LUB "Hej Mordo") z dismissem
(function call `zakoncz_rozmowe`) i 30s cooldownem (wake word pomija cooldown). Backend
(`main.py`/`ws_server.py`/`face.py`/`wake_word.py`/`gemini_client.py`) niezmieniony względem
architektury ESP32 — przeglądarka to po prostu kolejny klient WebSocket.
Natywne audio (sounddevice+tkinter) porzucone — twardy crash Windows przy mikrofon+głośnik+GUI
jednocześnie (szczegóły w ISSUE-019 → Problemy i rozwiązania).
`brain/main.py` dubluje logi do `brain/mordo.log` (nadpisywany co start).
Model Vosk PL (~50MB) w `brain/data/vosk-model-pl/` — gitignored, do ściągnięcia ręcznie na nowej
maszynie: https://alphacephei.com/vosk/models/vosk-model-small-pl-0.22.zip

EPIC-3 (Zadania Igora, Google Drive + głos) w toku: ISSUE-022 done — OAuth działa
(`brain/gdrive_auth.py`, `brain/credentials.json` + `brain/data/token.json` gitignored).

Co teraz: ISSUE-023 (magazyn zadań na Drive — format pliku, odczyt/zapis).
Next po EPIC-3: ISSUE-023→024→025, potem EPIC-2 (Hardware Mordo Faza 1) — ISSUE-011 (głośnik ESP32,
czeka na lutowanie) i ISSUE-018 (Gemini trigger przy rozpoznaniu twarzy na ESP32).

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-07-01 — EPIC-1 zamknięty (ISSUE-019/020/021/003). ISSUE-019: natywne audio (sounddevice+tkinter)
crashowało twardo (Windows 0xc0000005), przejście na przeglądarkę + istniejący ws_server.py. ISSUE-020:
kamera laptopa w przeglądarce, rozpoznawanie twarzy bez osobnego okna cv2. ISSUE-021: auto-trigger
powitania + dismiss przez function-call Gemini — po drodze bug (zgubiona pętla `while True` w
`_receive_audio` powodowała zapętlone powitania), znaleziony przez logi per-tura. ISSUE-003: wake word
"Hej Mordo" przez Vosk offline (PL) — ws_server.py rozsyła audio do wielu odbiorców (audio_callbacks).
Ustalono stały głos Gemini (Puck). Zaplanowano EPIC-3 (zadania Igora, Google Drive + głos) —
ISSUE-022 done: OAuth do Google Drive (`gdrive_auth.py`), Igor ręcznie założył projekt w GCP
i włączył Drive API.

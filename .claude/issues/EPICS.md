# Epics

## EPIC-1 — Software Mordo Faza 0 [done]

Pełna wersja Mordo działająca wyłącznie na laptopie — solidna baza przed powrotem do hardware.
Mikrofon + głośniki laptopa, kamera laptopa, rozpoznawanie twarzy, auto-trigger Gemini.

- [x] ISSUE-019 PC audio — rozmowa z Gemini przez mic + głośniki laptopa (przeglądarka)
- [x] ISSUE-020 Kamera laptopa — face recognition + zdjęcie referencyjne z przeglądarki
- [x] ISSUE-021 Auto-trigger — rozpoznanie Igora → powitanie → rozmowa lub dismiss (30s cooldown)
- [x] ISSUE-003 Wake word "Hej Mordo" — Vosk offline, aktywacja głosowa niezależna od twarzy

---

## EPIC-2 — Hardware Mordo Faza 1 [in-progress]

ESP32-S3 jako terminal sprzętowy: zbiera audio z mikrofonu I2S, wysyła przez WiFi/WebSocket do brain na PC, odbiera audio z brain i odtwarza przez głośnik.

- [x] ISSUE-006 Mikrofon ESP32-S3 Sense — działa, amplituda reaguje na głos
- [x] ISSUE-007 Jakość mikrofonu — nagranie testowe (16kHz, jakość dobra)
- [x] ISSUE-008 WiFi + WebSocket ESP32 ↔ brain — działa, streaming 1024B chunków
- [x] ISSUE-009 Pełna pętla audio: ESP32 mic → brain → Gemini → brain → głośnik PC — działa, multi-turn
- [x] ISSUE-010 Latencja i przerywanie: VAD 400ms + streaming playback + barge-in
- [ ] ISSUE-011 Głośnik ESP32 (MAX98357A I2S DAC) — wstrzymany, czeka na lutowanie + rozwiązanie konfliktu pinów z ekranem
- [x] ISSUE-012 Ekran LCD Round Display 1.28" (GC9A01) — stan Mordo wizualnie
- [x] ISSUE-013 Menu swipe — widok WiFi z siłą sygnału RSSI, interrupt-driven CHSC6X
- [x] ISSUE-014 Kamera ESP32 — inicjalizacja OV3660, stream JPEG do brain
- [x] ISSUE-015 Rozpoznawanie twarzy Igora w brain → "siema mordo" na ekranie
- [x] ISSUE-016 Widok kamery na LCD — carousel WIFI←MAIN→CAMERA swipe, 5fps
- [ ] ISSUE-018 Gemini trigger przy rozpoznaniu twarzy — wizja, powitanie w terminalu

---

## EPIC-3 — Zadania Igora (Google Drive + głos) [in-progress]

Mordo pamięta zadania Igora między sesjami (Google Drive), zarządza nimi głosem (dodawanie/edycja/
usuwanie/odhaczanie), i docelowo pomaga w planowaniu/dekompozycji/estymacji.
Świadome przeskoczenie kolejności faz (to Faza 2 "Pamięć" z `project-config.md`, Faza 1 hardware
jeszcze nie zamknięta) — decyzja Igora.

- [x] ISSUE-022 Google OAuth setup (Drive API) — autoryzacja, zapis/odświeżanie tokenu
- [ ] ISSUE-023 Magazyn zadań na Google Drive — format pliku, odczyt/zapis
- [ ] ISSUE-024 Zarządzanie zadaniami głosem — dodawanie/edycja/usuwanie/odhaczanie/lista (function-calling)
- [ ] ISSUE-025 Zasady planowania/dekompozycji/estymacji — instrukcje w system prompcie

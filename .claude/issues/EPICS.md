# Epics

## EPIC-1 — Software Mordo Faza 0 [in-progress, zawieszone]

Mordo działa na laptopie: widzi twarz Igora przez kamerę, słyszy go przez mikrofon, odpowiada głosem przez głośnik — wszystko przez Gemini Flash Live API.

- [ ] ISSUE-001 Gemini Live API + audio + system prompt (zawieszone — VAD niestabilny)
- [ ] ISSUE-002 Kamera
- [ ] ISSUE-003 Wake word "Hej Mordo"
- [ ] ISSUE-004 Rozpoznawanie twarzy Igora
- [ ] ISSUE-005 Symulacja okrągłego ekranu w przeglądarce

---

## EPIC-2 — Hardware Mordo Faza 1 [in-progress]

ESP32-S3 jako terminal sprzętowy: zbiera audio z mikrofonu I2S, wysyła przez WiFi/WebSocket do brain na PC, odbiera audio z brain i odtwarza przez głośnik.

- [x] ISSUE-006 Mikrofon ESP32-S3 Sense — działa, amplituda reaguje na głos
- [x] ISSUE-007 Jakość mikrofonu — nagranie testowe (16kHz, jakość dobra)
- [x] ISSUE-008 WiFi + WebSocket ESP32 ↔ brain — działa, streaming 1024B chunków
- [x] ISSUE-009 Pełna pętla audio: ESP32 mic → brain → Gemini → brain → głośnik PC — działa, multi-turn
- [x] ISSUE-010 Latencja i przerywanie: VAD 400ms + streaming playback + barge-in

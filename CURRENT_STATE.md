# Mordo — Stan Projektu

## Aktualna faza
Faza 1 — Hardware Mordo (ESP32-S3)

## Co jest zrobione
- Struktura projektu i agenci Claude Code
- ISSUE-006: Mikrofon ESP32-S3 Sense — firmware PDM działa
- ISSUE-007: Jakość mikrofonu — 16kHz, 16-bit, jakość dobra
- ISSUE-008: WiFi + WebSocket — ESP32 strumieniuje audio PCM do brain
- ISSUE-009: Pełna pętla audio — ESP32 mic → brain → Gemini → głośnik PC, multi-turn działa
- ISSUE-010: Streaming playback + barge-in + VAD 400ms/200ms — działa

## EPIC-2 status
Wszystkie issue zamknięte. Mordo słyszy przez ESP32, odpowiada przez Gemini, rozmawia wielokrotnie, można go przerywać.

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Co następne
- Do ustalenia z Igorem: następny epic / faza
- Kandydaci: głośnik na ESP32 (MAX98357A), wake word "Hej Mordo", kamera, ekran LCD

## Ostatnia sesja
2026-06-26 — ISSUE-010 ukończony: streaming playback (chunki grane natychmiast), barge-in (player_abort na interrupted), VAD skonfigurowany wg wzorca OmniBot. Repo publiczne na GitHubie.

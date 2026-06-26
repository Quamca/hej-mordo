# Mordo — Stan Projektu

## Aktualna faza
Faza 1 — Hardware Mordo (ESP32-S3)

## Co jest zrobione
- Struktura projektu i agenci Claude Code
- ISSUE-006: Mikrofon ESP32-S3 Sense — firmware PDM działa
- ISSUE-007: Jakość mikrofonu — 16kHz, 16-bit, jakość dobra
- ISSUE-008: WiFi + WebSocket — ESP32 strumieniuje audio PCM do brain
- ISSUE-009: Pełna pętla audio — ESP32 mic → brain → Gemini → głośnik PC, multi-turn działa

## EPIC-2 status
Wszystkie issue zamknięte. Mordo słyszy przez ESP32, odpowiada przez Gemini, rozmawia wielokrotnie.

## Co następne
- Backlog: latencja odpowiedzi
- Do ustalenia z Igorem: następny epic / faza

## Ostatnia sesja
2026-06-26 — EPIC-2 ukończony: pełna pętla głosowa działa, multi-turn naprawiony (while True wokół session.receive() + reconnect loop)

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

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S jest wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł.

## Co teraz
Próbujemy ekran LCD 1.28" okrągły (ISSUE-012).
Uwaga: styki ekranu mogą mieć ten sam problem co głośnik, ale SPI/I2C jest
mniej wrażliwe niż I2S audio — artefakty wizualne łatwiejsze do tolerowania niż glitche dźwiękowe.

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-26 — ISSUE-011 zaimplementowany ale wstrzymany (lutowanie). Przechodzimy do ISSUE-012 ekran LCD.

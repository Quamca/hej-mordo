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
- ISSUE-012: Ekran LCD Round Display — GC9A01 + LovyanGFX, stany IDLE/LISTEN/SPEAK wyświetlane poprawnie

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Co teraz
Wszystkie aktywne issue zamknięte. Następny krok: wybrać nowe issue z backlogu lub zacząć ISSUE-011 po lutowaniu.

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-27 — ISSUE-012 zrobiony: ekran pokazuje szary/niebieski/zielony okrąg ze stanem Mordo. Fix: invertDisplay(true) dla GC9A01 na Seeed Round Display.

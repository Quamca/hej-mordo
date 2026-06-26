# ISSUE-011 — Głośnik ESP32 (MAX98357A I2S DAC)

**Status:** planned
**Epic:** EPIC-2

## Cel

Audio z Gemini gra przez głośnik podłączony do ESP32 zamiast przez głośniki PC.

## Acceptance criteria

- [ ] Brain wysyła audio PCM do ESP32 przez WebSocket
- [ ] ESP32 odtwarza audio przez MAX98357A (I2S)
- [ ] Jakość głosu akceptowalna (brak glitchy, brak clipping)
- [ ] Self-interruption zredukowany (echo mniejsze niż przy PC speakers)

## Kontekst

Aktualnie brain odbiera audio z Gemini i gra je przez głośniki PC (`sounddevice`).
Głośniki PC są daleko od ESP32 — mikrofon ESP32 słyszy Mordo i odsyła jego głos
z powrotem do Gemini (self-interruption). Głośnik fizyczny na ESP32 rozwiązuje to
akustycznie, a w kolejnym kroku otwiera drogę do AEC (ESP-ADF).

## Zakres

- Firmware: odbiór chunków PCM przez WebSocket, I2S output do MAX98357A
- Brain: zamiast `sounddevice` → wysyłanie audio do ESP32 przez WebSocket
- Config: sample rate, pin I2S (BCLK, LRCLK, DIN)

## Hardware

- Wzmacniacz MAX98357A I2S DAC (już w zestawie)
- Głośnik 8Ω 2W (już w zestawie)
- Piny I2S na Xiao ESP32-S3: do ustalenia przy podłączaniu

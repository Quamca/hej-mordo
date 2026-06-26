---
title: "ISSUE-006: Mikrofon wbudowany ESP32-S3 Sense — test i odczyt audio"
status: done
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-26
updated: 2026-06-26
---

## Cel

Potwierdzić że wbudowany mikrofon PDM na XIAO ESP32-S3 Sense działa — odczytuje audio i wysyła amplitudę na Serial Monitor.

## Acceptance Criteria

- [x] Firmware kompiluje się i wgrywa przez PlatformIO
- [x] Serial Monitor pokazuje wartości amplitudy
- [x] Wartości reagują na głos (rosną gdy Igor mówi, niskie przy ciszy)

## Notatki

Mikrofon XIAO ESP32-S3 Sense to PDM (nie klasyczny I2S).
API: ESP32 Arduino core 3.x używa `ESP_I2S.h`.
Test tylko przez Serial — bez WiFi, bez brain.

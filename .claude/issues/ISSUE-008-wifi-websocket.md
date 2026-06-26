---
title: "ISSUE-008: WiFi + WebSocket ESP32 ↔ brain"
status: done
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-26
updated: 2026-06-26
---

## Cel

ESP32-S3 łączy się z WiFi i strumieniuje chunki audio PCM przez WebSocket do brain na PC.

## Acceptance Criteria

- [x] ESP32 łączy się z WiFi (WPA2)
- [x] ESP32 otwiera WebSocket do brain i utrzymuje połączenie
- [x] Brain odbiera binary chunki PCM (1024B = 512 sampli @ 16kHz)
- [x] Brain loguje połączenie i chunki

## Notatki

Wymaga anteny IPEX podpiętej do złącza na płytce — bez niej WiFi nie działa.
Dane WiFi i IP brain w `firmware/include/secrets.h` (gitignored).
Brain: `python brain/ws_server.py` — serwer WebSocket z asyncio.Queue.

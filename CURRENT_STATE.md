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
- ISSUE-013: Menu swipe — widok WiFi z siłą sygnału (RSSI kreski) i SSID. Interrupt-driven (CHSC6X FALLING edge).
- ISSUE-014: Kamera ESP32 OV3660 — stream JPEG ~5fps do brain przez WebSocket (CAM\0 header).
- ISSUE-015: Rozpoznawanie twarzy Igora (InsightFace buffalo_sc) — ekran "siema" na zielonym tle.
- ISSUE-016: Widok kamery na LCD — carousel WIFI←MAIN→CAMERA swipe, obraz 5fps na ekranie.

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## AKTUALNY BUG — ekran czarny po cold boot (USB power cycle)

### Symptom
Po odłączeniu i ponownym podłączeniu USB ekran jest czarny (podświetlony, ale bez treści).
Po warm reset (upload przez PlatformIO) ekran działa — GC9A01 zostaje zasilony podczas uploadu.

### Diagnoza (potwierdzona)
GC9A01 na Seeed Round Display for XIAO **nie ma NRST podłączonego do żadnego GPIO XIAO**.
Potwierdzenie: Zephyr device tree overlay dla tego shielda nie zawiera `reset-gpios`.
Reset sprzętowy GC9A01 odbywa się wyłącznie przez RC circuit lub pin RST XIAO (nie programowalny).

Dodatkowe info: D6 (GPIO43, TX) = backlight — Zephyr wyłącza Serial na tym boardzie ze względu na konflikt.

### Co próbowaliśmy (bez efektu na cold boot)
- Różne ustawienia pin_rst (-1, 43)
- delay() przed displayInit: 50ms, 200ms, 300ms, 5000ms
- BOARD_HAS_PSRAM
- SD_CS (GPIO3) HIGH przed tft.init()
- Display CS (GPIO2) HIGH przed tft.init()
- CS piny HIGH jako pierwsze linie setup() (przed delay)
- double-reset: esp_restart() przy ESP_RST_POWERON
- SPI freq 40MHz zamiast 80MHz
- Fizyczne odpięcie i wpięcie Round Display
- Upload zarówno test_display (minimalny) jak i głównego firmware

### Rozwiązania do wyboru
1. **Akumulator** — Li-Pol podłączony do JST PH 1.25mm na XIAO; GC9A01 nie traci zasilania przy USB reconnect → cold boot znika. Igor ma 4000mAh w planie, trzeba sprawdzić złącze.
2. **Pull-up rezystor** — 10kΩ między GPIO2 (D1) a 3.3V; utrzymuje Display CS HIGH podczas bootloadera zanim setup() startuje. Proste lutowanie.
3. **Upload** — naprawia jeśli SPI nie było wcześniej zepsute; nie gwarantowane po każdym cold boot.

## Co teraz (po naprawie ekranu)
ISSUE-018 — Gemini odpala się gdy Mordo rozpozna Igora, dostaje klatki kamery (wizja), wita go tekstem w terminalu.

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-28 — cały dzień na debug cold boot ekranu. Bug nie rozwiązany softwareowo.
Diagnoza potwierdzona: brak GPIO dla NRST GC9A01. Następna sesja: wybrać rozwiązanie (akumulator / pull-up / zaakceptować).

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

## AKTUALNY BUG — ekran czarny po power cycle

### Symptom
Po odłączeniu i ponownym podłączeniu USB ekran jest czarny (podświetlony, ale bez treści).
Firmware działa poprawnie — Serial Monitor pokazuje komendy rysowania. SPI do GC9A01 nie dociera.

### Co już próbowaliśmy (bez efektu)
- Różne ustawienia pin_rst (-1, 43)
- delay() przed displayInit (50ms, 200ms, 300ms)
- BOARD_HAS_PSRAM dodane do test_display env
- SD_CS (GPIO3) HIGH przed tft.init()
- Fizyczne odpięcie i wpięcie modułu Round Display
- Upload zarówno test_display (minimalny) jak i głównego firmware

### Konfiguracja SPI (display.cpp i test_display.cpp)
- SCK=7, MOSI=9, MISO=8, DC=4, CS=2, RST=-1
- SPI2_HOST, 40–80 MHz
- Ekran: Panel_GC9A01, 240×240, invertDisplay(true)
- SD_CS=3 (Round Display ma SD na tym samym SPI)

### Co wiadomo
- Backlight (GPIO43) działa — ekran jest podświetlony
- Swipe/touch (CHSC6X GPIO44) działał przed bugiem
- MAX98357A fizycznie odłączony od początku
- Kamera OV3660 na XIAO Sense — piny nie kolidują z SPI

### Hipotezy do sprawdzenia w następnej sesji
1. GC9A01 NRST — sprawdzić schemat Seeed Round Display (104030087) do którego pinu XIAO jest podłączony NRST kontrolera LCD. Jeśli do XIAO RST, to przy USB reconnect powinien resetować się sam.
2. Oficjalny przykład Seeed — sprawdzić jak Seeed inicjalizuje GC9A01 w swoich przykładach (repozytorium Seeed_Arduino_RoundDisplay)
3. Sprawdzić czy problem nie jest w tym że kamera (cameraInit) robi coś z SPI2 lub GPIO — przetestować test_display bez cameraInit

## Co teraz (po naprawie ekranu)
ISSUE-018 — Gemini odpala się gdy Mordo rozpozna Igora, dostaje klatki kamery (wizja), wita go tekstem w terminalu.

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-27 — cały dzień na debug ekranu. Bug nie rozwiązany. Następna sesja: sprawdzić schemat NRST + oficjalny przykład Seeed.

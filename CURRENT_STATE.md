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

## Co teraz
DEBUG ekranu — ekran świeci czarne tło (backlight ON) ale nie wyświetla nic po cold boot.

### Stan debugowania (2026-06-28, popołudnie)
Objaw: ekran podświetlony ale czarny. Raz zadziałał poprawnie, po reconnect znów czarny.
Hipotezy zidentyfikowane:
- `pin_rst = -1` w LovyanGFX — GC9A01 bez hardware resetu, może być w losowym stanie po cold boot
- `cameraInit()` w main.cpp wywoływana PO `displayInit()` — może przerekonfigurować SPI/DMA
- Pin 43 = backlight (nie reset GC9A01 jak mylnie opisano w commit `eaf5a92`)
- `display.cpp` nie ma `pinMode(43, OUTPUT)` — backlight trzyma UART TX (działa ale niezawodnie)

**Następny krok: Krok 2 z planu** — wgraj `test_display` env (izolowany test bez kamery/WiFi/swipe):
```
pio run -e test_display --target upload
```
Build OK (340KB), ale Igor odłączył urządzenie przed uploadem — stąd błąd COM3.
Po powrocie: podłącz ESP32, wgraj `test_display` w VS Code (env: test_display), sprawdź czy ekran pokazuje kolory.

Plik z planem debugowania: `TEMP-debug-ekran.md` (usunąć po zakończeniu).

## ISSUE-011 — wstrzymany (czeka na lutowanie)
Implementacja gotowa (firmware + brain + test_speaker.py).
Problem: luzy na stykach MAX98357A — audio I2S wrażliwe na przerwy.
Wrócimy gdy Igor przylutuje moduł. Przy lutowaniu zmienić piny głośnika (konflikt z ekranem na D7/D8).

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-28 — debug ekranu (cold boot czarny). Poprzednia sesja: downgrade espressif32 @ 6.7.0 naprawił cold boot, ale po kolejnym odłączeniu ekran znów nie działa. Diagnoza w toku.

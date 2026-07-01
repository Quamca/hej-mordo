# ISSUE-012 — Ekran LCD Round Display

**Status:** done
**Epic:** EPIC-2

## Cel

Wyświetlacz pokazuje stan Mordo — reaguje wizualnie na rozmowę.

## Hardware

- Seeed Round Display for XIAO (104030087)
- 1.28" IPS LCD 240×240px
- Sterownik: GC9A01 (SPI)
- Dotyk: CST816S (I2C)
- Podłączenie: bezpośrednio na piny XIAO (bez kabli)

## Acceptance criteria

- [ ] Ekran się inicjalizuje i pokazuje cokolwiek (test koloru / kółko)
- [ ] Mordo pokazuje stan: słucha / mówi / czeka
- [ ] Dotyk odczytywany (nawet jeśli nie używany jeszcze)

## Konflikt pinów z głośnikiem

Ekran zajmuje D7 (GPIO44) i D8 (GPIO7) — te same co głośnik MAX98357A.
Nie można używać obu jednocześnie na obecnym okablowaniu.
Rozwiązanie przy lutowaniu: przenieść głośnik na wolne piny (np. D2/D3/D10).

## Biblioteka

`Seeed_Arduino_RoundDisplay` przez lib_deps w platformio.ini.
Zawiera sterownik GC9A01 + obsługę dotyku CST816S.

## Problemy i rozwiązania

**Pozorny cold boot bug — w rzeczywistości problem fizyczny**
Przez cały dzień debugowaliśmy oprogramowanie (SPI timing, pin_rst, BOARD_HAS_PSRAM).
Prawdziwa przyczyna: brak lutowania pinów Round Display → nieregularny kontakt → ekran gaśnie przy ruchu.
Rozwiązanie: przylutować piny. Do tego czasu ekran jest niestabilny sprzętowo.

**Cold boot — ekran nie startuje po odłączeniu zasilania**
Objaw: ekran działa po USB reconnect, ale nie po zimnym starcie (odłączony akumulator/USB).
Przyczyna: ESP32 Arduino Core 3.x ma błąd taktowania SPI przy cold boot na XIAO + Round Display.
Fix: downgrade `espressif32 @ 6.7.0` (Arduino Core 2.0.16) w `platformio.ini`.
Jedna linia — cały dzień debugowania. Nie upgradować `espressif32` bez sprawdzenia tego.

**Ekran nie odświeżał się po reconnect USB**
Objaw: po podłączeniu USB ekran był biały lub zamrożony.
Fix: hardware reset GC9A01 przez pin 43 przy inicjalizacji.

**Touch controller — błędna biblioteka**
Chip to CHSC6X (I2C 0x2e), NIE CST816S mimo że dokumentacja Seeed mówi inaczej.
Używać `Seeed_Arduino_RoundDisplay` która obsługuje CHSC6X.

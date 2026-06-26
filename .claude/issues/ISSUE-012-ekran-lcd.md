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

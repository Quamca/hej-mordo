---
title: "ISSUE-007: Jakość mikrofonu — nagranie testowe i strojenie parametrów"
status: done
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-26
updated: 2026-06-26
---

## Cel

Ocenić jakość audio z mikrofonu PDM i dobrać optymalne parametry przed integracją z Gemini.

## Acceptance Criteria

- [x] Firmware nagrywa 5 sekund i zrzuca PCM przez Serial
- [x] Skrypt Python zapisuje dane jako plik `.wav`
- [x] Igor odsłuchuje nagranie i ocenia jakość
- [x] Parametry mikrofonu ustalone jako optymalne (lub znane ograniczenia)

## Notatki

Baseline z ISSUE-006: ~1350 przy ciszy, do ~3744 przy głosie.
Wynik: 16kHz, 16-bit — jakość dobra, zatwierdzone przez Igora.

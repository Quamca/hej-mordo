---
title: "ISSUE-016: Podgląd kamery na ekranie LCD ESP32"
status: planned
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-27
updated: 2026-06-27
---

## Cel

ESP32 wyświetla obraz z kamery na okrągłym ekranie LCD jako nowy widok w menu swipe.

## Acceptance Criteria

- [ ] Nowy widok VIEW_CAMERA dostępny przez swipe right z VIEW_WIFI
- [ ] Ekran pokazuje live feed z kamery (~2fps)
- [ ] Obraz 320x240 przycięty/przeskalowany do 240x240 (centrum klatki)
- [ ] Swipe left z VIEW_CAMERA wraca do VIEW_WIFI
- [ ] Brain nadal odbiera klatki do rozpoznawania twarzy (równolegle)

## Notatki

- LovyanGFX ma wbudowany `drawJpg(data, len, x, y, w, h)` — JPEG decode bez dodatkowych bibliotek
- Rysowanie co 500ms (2fps) żeby nie blokować pętli audio
- Rogi obrazu prostokątnego wychodzą poza okrągły ekran — niewidoczne, nie ma problemu

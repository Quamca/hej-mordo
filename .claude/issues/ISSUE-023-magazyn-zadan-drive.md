---
title: "ISSUE-023: Magazyn zadań na Google Drive"
status: planned
type: issue
faza: 2
epic: EPIC-3
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Lista zadań Igora żyje jako plik na jego Google Drive — przetrwa restart brain, zmianę komputera,
i jest widoczna też poza Mordo (Igor może zajrzeć na Drive i zobaczyć surowe dane).

## Acceptance Criteria

- [ ] Plik z zadaniami (JSON) tworzony na Drive Igora przy pierwszym uruchomieniu (jeśli nie istnieje)
- [ ] Funkcja odczytu: pobiera aktualną listę zadań z Drive
- [ ] Funkcja zapisu: nadpisuje plik na Drive nową wersją listy
- [ ] Format zadania: treść, status (do zrobienia/w trakcie/zrobione), opcjonalnie szacowany czas, data

## Notatki

- Reużywa autoryzację z ISSUE-022
- Dokładna struktura pola zadania — do doprecyzowania przy implementacji
- Zależność: ISSUE-022 done

## Test manualny

1. Pierwsze uruchomienie → plik zadań pojawia się na Drive Igora
2. Ręczna zmiana w kodzie (dodanie testowego zadania) → widoczne po odświeżeniu pliku na Drive

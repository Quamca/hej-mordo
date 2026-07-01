---
title: "ISSUE-023: Magazyn zadań na Google Drive"
status: done
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

- [x] Plik z zadaniami (JSON) tworzony na Drive Igora przy pierwszym uruchomieniu (jeśli nie istnieje)
- [x] Funkcja odczytu: pobiera aktualną listę zadań z Drive
- [x] Funkcja zapisu: nadpisuje plik na Drive nową wersją listy
- [x] Format zadania: treść, status (do zrobienia/w trakcie/zrobione), opcjonalnie szacowany czas, data

## Notatki

- Nowy moduł: `brain/tasks_store.py` — plik `mordo_zadania.json` na Drive (nazwa stała, wyszukiwany po nazwie)
- Reużywa autoryzację z ISSUE-022 (`gdrive_auth.get_drive_service()`)
- Format zadania: `{"id", "text", "status", "estimate", "date"}` — `id` to identyfikator do przyszłej
  edycji/usuwania (ISSUE-024), `estimate`/`date` opcjonalne (mogą być `None`)
- `load_tasks()`/`save_tasks()` operują na całej liście naraz (nadpisanie) — dodawanie/edycja
  pojedynczych zadań to logika ISSUE-024, budowana na tych dwóch prymitywach
- `_file_id_cache` — plik wyszukiwany raz, potem ID w pamięci (unika zbędnych zapytań `list()`)
- Zależność: ISSUE-022 done

## Test manualny

1. Pierwsze uruchomienie (`python tasks_store.py`) → plik `mordo_zadania.json` pojawia się na Drive Igora
2. Zapis testowego zadania (`save_tasks([...])`) w jednym procesie
3. Świeży proces Pythona (bez cache) → `load_tasks()` widzi to samo zadanie — potwierdzona realna
   persystencja na Drive, nie tylko lokalny cache
4. Igor potwierdził wizualnie na drive.google.com że plik istnieje

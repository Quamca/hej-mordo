---
title: "Proaktywne przypomnienia i lista zadań"
type: note
faza: 3
created: 2026-06-25
---

## Pomysł

Mordo przyjmuje polecenia głosowe do zapisywania przypomnień i zadań. Gdy brakuje informacji (np. godzina przypomnienia) — pyta. Gdy wykryje Igora kamerą, proaktywnie zagaduje i przypomina o zaległych zadaniach — ale z wyczuciem: ocenia co Igor robi i dopasowuje ton (samo przypomnienie vs aktywna propozycja "to może teraz?").

## Przykłady z rozmowy

- "przypomnij mi, żebym przed wyjazdem do kuzynki zapakował do samochodu basen i taker" → jeśli brak godziny, pyta kiedy
- "zapisz na liście rzeczy do zrobienia, że mam wywalić śmieci dzisiaj" → zapisuje, odpowiada "ok"
- Mordo widzi Igora kamerą → zagaduje "Hej Igor, co robisz?" → na podstawie odpowiedzi ocenia priorytet → jeśli Igor robi coś ważniejszego: "tylko przypominam, że masz śmieci do wywalenia" → jeśli Igor robi coś mało ważnego: "to może wywalisz śmieci? Będzie z głowy"

## Komponenty (wstępnie)

- Przyjmowanie przypomnień/zadań głosowo + zapis
- Zadawanie pytań doprecyzowujących gdy brak danych
- Integracja z Google Calendar / listą zadań
- Proaktywne zagadywanie po wykryciu twarzy kamerą
- Ocena kontekstu (co Igor robi) i dopasowanie tonu/pilności

## Zależności

- Wymaga: ISSUE-005 (rozpoznawanie twarzy), Faza 2 (pamięć, Google Drive), Faza 3 (kalendarz, mail)

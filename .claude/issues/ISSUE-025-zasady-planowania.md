---
title: "ISSUE-025: Zasady planowania, dekompozycji i estymacji zadań"
status: planned
type: issue
faza: 2
epic: EPIC-3
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Gemini nie tylko zapisuje zadania 1:1 to co Igor powie, ale aktywnie pomaga: dopytuje o kontekst,
rozbija złożone zadania na mniejsze kroki, szacuje czas, sugeruje priorytety.

## Acceptance Criteria

- [ ] Do ustalenia z Igorem przy starcie tego issue — konkretne zasady dekompozycji/estymacji
      jeszcze nie zdefiniowane (celowo, żeby nie zgadywać czego Igor nie powiedział)

## Notatki

- To instrukcje w system prompcie (podobnie jak `SYSTEM_PROMPT`/`_GREETING_PROMPT` w `gemini_client.py`),
  nie nowa mechanika techniczna
- Ma sens dopiero po ISSUE-024 (Gemini musi już umieć czytać/zapisywać zadania)
- Przed startem implementacji: krótka sesja ustalająca dokładne zasady (jak Igor chce być dopytywany,
  jakie kryteria estymacji, jak wygląda dobra dekompozycja z jego perspektywy)
- Zależność: ISSUE-024 done

## Test manualny

Do zdefiniowania razem z Acceptance Criteria, przy starcie tego issue.

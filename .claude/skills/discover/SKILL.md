---
name: discover
description: 'Sesja odkrywania nowych pomysłów i kierunku dla projektu Mordo. Używaj gdy Igor mówi "mam pomysł", "nowa funkcja", "co powiesz na", "chciałbym żeby Mordo", lub gdy zaczyna się planowanie nowej fazy. Kończy się zapisanym issue lub notatką.'
---

# /discover — Odkrywanie Pomysłów

## Setup

Przeczytaj `.claude/rules/project-config.md` — znaj aktualną fazę projektu.

## Krok 1 — Zbierz kontekst (max 3 pytania)

Jeśli Igor nie dał wystarczającego kontekstu, zadaj max 3 pytania naraz:

```
Mam kilka pytań zanim zapiszemy pomysł:

1. Co konkretnie Mordo ma robić? (z perspektywy użytkownika — co widzisz/słyszysz)
2. To nowa funkcja, zmiana czegoś istniejącego, czy bug?
3. Czy to na teraz (aktualna faza) czy "kiedyś"?
```

Pomiń pytania których odpowiedź już padła.

## Krok 2 — Klasyfikuj

| Sygnał | Typ |
|---|---|
| Duża zmiana, wiele komponentów, wiele sesji | `epic` — rozbij na issues |
| Jedna konkretna zmiana, ≤ kilka plików | `issue` |
| "Nie wiem czy da się" — ryzyko techniczne | `spike` |
| Luźna obserwacja, "może kiedyś" | `note` — quick-notes |
| Coś zepsutego | `bug` |

## Krok 3 — Sprawdź fazę

Czy pomysł pasuje do aktualnej fazy projektu?
- Jeśli tak → zapisz jako `issue` lub `epic`
- Jeśli nie → zapisz jako `note` z adnotacją "Faza N"

## Krok 4 — Zaproponuj gdzie ląduje

```
Klasyfikuję to jako [issue/epic/spike/note].
[Jeśli issue]: Zapiszę w {issues}/ISSUE-NNN-slug.md
[Jeśli note]: Zapiszę w {issues}/notes/quick-note-YYYY-MM-DD.md

Zapisać? (t/n)
```

## Krok 5 — Zapisz (po "t")

**Issue:**
```markdown
---
title: "ISSUE-NNN: Krótki tytuł"
status: planned
type: issue
faza: N
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Cel

{1-2 zdania — co Igor zobaczy/usłyszy gdy to działa}

## Acceptance Criteria

- [ ] AC 1
- [ ] AC 2

## Notatki

{opcjonalnie — edge cases, zależności}
```

**Epic** — dodaj sekcję do `{issues}/EPICS.md` (cel + lista sub-issues). Nie twórz osobnego pliku dla epica. Rozbij na sub-issues w tej samej sesji jeśli Igor chce zacząć.

## Zasady

- Max 3 pytania naraz
- Nie wymyślaj AC których Igor nie podał — zapytaj
- Zawsze zakończ z plikiem lub "nie zapisujemy, bo X"

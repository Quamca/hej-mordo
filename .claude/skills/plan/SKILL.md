---
name: plan
description: 'Planowanie implementacji przed kodowaniem. Używaj gdy /dev ma zrobić coś nietrywialnego — wiele plików, nowy moduł, integracja z API, zmiana architektury. Dla prostych bugfixów pomiń.'
---

# /plan — Planowanie Implementacji

## Kiedy używać

- Nowy moduł (np. nowy skill Mordo, integracja z API)
- Zmiana dotykająca > 2 plików
- Coś co może złamać istniejące funkcje
- Niejasne jak to zrobić

Dla prostych zmian (1 plik, oczywiste) → idź prosto do `/dev`.

## Setup

1. Przeczytaj `{issues}/ISSUE-NNN-*.md` — AC = definicja "gotowe"
2. Przeczytaj `project-config.md` — stack, faza, ścieżki

## Krok 1 — Analiza

- Co się zmienia vs co zostaje?
- Które pliki są dotknięte?
- Czy są zależności (zewnętrzne API, inne moduły)?
- Jakie ryzyko (co może się zepsuć)?

## Krok 2 — Plan kroków

```markdown
## Plan — ISSUE-NNN: {tytuł}

### Ryzyka
1. {największe ryzyko}
2. ...

### Pliki do zmiany/stworzenia
| Plik | Akcja | Powód |
|---|---|---|
| brain/skills/X.py | stwórz | nowy skill |
| brain/agent.py | modyfikuj | rejestracja skilla |

### Kolejność implementacji
1. {krok 1 — fundament}
2. {krok 2}
3. {testy}

### Test manualny
- Co wpisać/powiedzieć żeby przetestować?
- Czego oczekiwać?
```

## Zasady

- STOP jeśli AC jest niejasne — zapytaj przed planem
- Plan w odpowiedzi czatu — nie twórz pliku (chyba że Igor prosi)
- Po planie Igor decyduje czy kontynuować z `/dev`

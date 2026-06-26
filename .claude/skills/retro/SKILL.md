---
name: retro
description: 'Retrospektywa po zakończeniu fazy projektu lub na życzenie. Podsumowuje co poszło dobrze, co nie, jakie decyzje architektoniczne zapadły. Aktualizuje project-config jeśli coś się zmieniło.'
---

# /retro — Retrospektywa

## Kiedy używać

- Po zakończeniu fazy projektu
- Po serii issues które coś zmieniły architektonicznie
- Na życzenie Igora

## Krok 1 — Zbierz dane

Przejrzyj zamknięte issues z ostatniego okresu:
```bash
grep -l "status: done" {issues}/*.md
```

## Krok 2 — Retro (3 sekcje)

```markdown
## Retro — {data lub "Faza N"}

### Co poszło dobrze
- {obserwacja}

### Co nie poszło / utrudniało
- {obserwacja}

### Decyzje architektoniczne które zapadły
- {decyzja i powód — do pamięci na przyszłość}

### Na następną fazę
- {zmiana procesu lub priorytetu}
```

## Krok 3 — Aktualizuj jeśli potrzeba

Jeśli zmieniło się coś w stacku, fazach lub ścieżkach → zaproponuj update `project-config.md`.
Czekaj na OK przed zapisem.

## Zasady

- Retro w pliku tylko jeśli Igor chce zachować — domyślnie tylko w czacie
- Nie oceniaj Igora — tylko proces i decyzje techniczne

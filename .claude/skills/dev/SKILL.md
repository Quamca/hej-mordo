---
name: dev
description: 'Implementacja kodu dla projektu Mordo. Firmware (MicroPython/ESP32), brain (Python/PC), integracje API, dokumentacja HTML. Używaj po /plan lub bezpośrednio dla prostych tasków.'
---

# /dev — Implementacja

## Setup

1. Przeczytaj issue: `{issues}/ISSUE-NNN-*.md` — AC = definicja "gotowe"
2. Przeczytaj `project-config.md` — stack, faza, ścieżki
3. Sprawdź `git status` — musi być czysto przed startem

## Limit plików (zawsze)

Przed każdą edycją sprawdź liczbę linii (`wc -l`).
**Plik > 230 linii = STOP** — podziel na moduły, opisz podział, czekaj na OK.

## Analiza przed kodem

Zanim napiszesz pierwszą linię, powiedz:
1. Które pliki tworzę/modyfikuję
2. Największe ryzyko (1-2 zdania)
3. Czy coś może się zepsuć

Dla trywialnych bugfixów — skróć do 1 zdania.

## Implementacja

### Kolejność (brain/Python)
moduł/klasa → integracja → rejestracja w agencie → test

### Kolejność (firmware/MicroPython)
driver/helper → główna logika → integracja w main.py → test na urządzeniu

### Styl kodu
- Komentarze opisują CO i DLACZEGO, nie jak
- Bez odniesień do issue/sprintu/agentów w komentarzach
- Funkcje < 30 linii (extract jeśli większe)

## Błąd podczas testu

STOP. Format:
```
Błąd: {krótki opis co poszło nie tak}
Przyczyna: {co wywołuje błąd}
Propozycja: {konkretna zmiana do wprowadzenia}
```
Czekaj na "ok" przed wprowadzeniem zmiany.

## Konflikt / sprzeczność

STOP. Format:
```
⚠️ Widzę sprzeczność:
- Issue mówi: "X"
- Kod/rzeczywistość mówi: "Y"

Opcja 1: {zgodnie z issue}
Opcja 2: {zgodnie z rzeczywistością}
```
Czekaj na wybór.

## Po implementacji

Podsumowanie:
```
## Zrobione — ISSUE-NNN

Zmienione pliki:
- {plik} — {co zrobiono}

AC checklist:
- [x] AC 1
- [x] AC 2

Test manualny: {co przetestować i jak}
```

Następnie: **czekaj na "działa" od Igora** przed commitem.

## Commit (tylko po "commit now")

```bash
git add {zmienione pliki}
git commit -m "[ISSUE-NNN] feat: opis

- zmiana 1
- zmiana 2"
```

Potem: `git push` tylko po "push now".

## Zasady

- Nigdy nie commituj/pushuj bez zgody Igora
- Firmware testowany jest tylko na urządzeniu — nie ma emulatora
- Jeśli task > 1 sesja → commit każdy działający krok osobno

---
title: "ISSUE-024: Zarządzanie zadaniami głosem (function-calling)"
status: planned
type: issue
faza: 2
epic: EPIC-3
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Igor mówi do Mordo "dodaj zadanie...", "co mam do zrobienia?", "oznacz X jako zrobione",
"usuń zadanie Y" — Gemini wykonuje to na liście zadań z ISSUE-023, głosem.

## Acceptance Criteria

- [ ] Dodawanie zadania głosem → zapis na Drive
- [ ] Odczyt listy zadań głosem → Gemini czyta na głos co jest do zrobienia
- [ ] Edycja istniejącego zadania głosem
- [ ] Usuwanie zadania głosem
- [ ] Oznaczanie zadania jako zrobione głosem
- [ ] Zmiany widoczne w kolejnej sesji (persystencja przez Drive z ISSUE-023)

## Notatki

- Wzorzec: function-calling jak `zakoncz_rozmowe` z ISSUE-021 — kilka nowych funkcji
  (`dodaj_zadanie`, `edytuj_zadanie`, `usun_zadanie`, `oznacz_zrobione`, `pokaz_zadania`)
- Dostępność w każdej sesji Gemini (nie tylko powitalnej) — do ustalenia przy implementacji
- Zależność: ISSUE-023 done

## Test manualny

1. "Dodaj zadanie: kup mleko" → potwierdzenie głosem, zadanie na liście
2. "Co mam do zrobienia?" → Gemini wymienia zadania
3. "Oznacz kup mleko jako zrobione" → status się zmienia
4. "Usuń zadanie kup mleko" → znika z listy
5. Restart brain → zadania nadal tam są (z Drive)

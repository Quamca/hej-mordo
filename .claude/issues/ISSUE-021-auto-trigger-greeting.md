---
title: "ISSUE-021: Auto-trigger Gemini przy rozpoznaniu twarzy + greeting + dismiss"
status: planned
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Mordo rozpoznaje Igora → automatycznie startuje sesję Gemini z powitaniem. Jeśli Igor powie "nie dzięki" (lub podobnie) → Gemini kończy sesję i wraca do czekania.

## Acceptance Criteria

- [ ] Rozpoznanie Igora triggeruje Gemini (nie czeka na wake word)
- [ ] Gemini dostaje system prompt powitalny: "Igor jest w zasięgu, przywitaj go i zapytaj czy możesz pomóc"
- [ ] Gemini mówi "Siema mordo, mogę w czymś pomóc?" (lub podobnie)
- [ ] Normalna odpowiedź → kontynuuje rozmowę
- [ ] Dismiss ("nie dzięki", "nie teraz", "spoko", itp.) → Gemini kończy sesję, wraca do nasłuchu twarzy
- [ ] Po dismiss — Mordo nie triggeruje ponownie przez ~30s (cooldown)
- [ ] Jeśli Igor wyjdzie z kadru i wróci → trigger odpala się znowu

## Notatki

- Dismiss wykrywa Gemini sam (przez system prompt z instrukcją zakończenia)
- Alternatywa: brain wykrywa słowa kluczowe w transkrypcji i kończy sesję
- Cooldown 30s zapobiega natychmiastowemu re-triggerowi po dismiss
- Tryb: dwa stany — `IDLE` (nasłuch twarzy) i `SESSION` (aktywna rozmowa z Gemini)
- Zależność: ISSUE-019 + ISSUE-020 done

## Test manualny

1. `python pc_mordo.py` → Mordo w trybie IDLE
2. Stań przed kamerą → Gemini wita ("Siema mordo...")
3. Odpowiedz "nie dzięki" → cisza, Mordo wraca do IDLE
4. Zostań przed kamerą — przez 30s brak triggera
5. Wyjdź i wróć po 30s → Gemini znowu wita

---
title: "ISSUE-024: Zarządzanie zadaniami głosem (function-calling)"
status: done
type: issue
faza: 2
epic: EPIC-3
created: 2026-07-01
updated: 2026-07-02
---

## Cel

Igor mówi do Mordo "dodaj zadanie...", "co mam do zrobienia?", "oznacz X jako zrobione",
"usuń zadanie Y" — Gemini wykonuje to na liście zadań z ISSUE-023, głosem.

## Acceptance Criteria

- [x] Dodawanie zadania głosem → zapis na Drive
- [x] Odczyt listy zadań głosem → Gemini czyta na głos co jest do zrobienia
- [x] Edycja istniejącego zadania głosem (współdzieli `_find_task` z potwierdzonym usuwaniem/odhaczaniem)
- [x] Usuwanie zadania głosem
- [x] Oznaczanie zadania jako zrobione głosem
- [x] Zmiany widoczne w kolejnej sesji (persystencja przez Drive z ISSUE-023)

## Podejście — rozszerzone o widok w przeglądarce (poza pierwotnym zakresem)

Przy okazji dodano panel zadań w `pc_mordo.html`/`pc_mordo.js` — lista na żywo (push przez WebSocket
po każdej zmianie, głosowej lub ręcznej), plus ręczne dodawanie/odhaczanie/edycja/usuwanie z poziomu
przeglądarki. To wykraczało poza AC tego issue (które dotyczyło tylko głosu), ale naturalnie pasowało
do tej samej sesji roboczej.

## Notatki

- Wzorzec: function-calling jak `zakoncz_rozmowe` z ISSUE-021 — `task_tools.py` definiuje
  `TOOL_DECLARATIONS` (dodaj_zadanie, edytuj_zadanie, usun_zadanie, oznacz_zrobione, pokaz_zadania)
  i `HANDLERS` (dispatch po nazwie funkcji)
- Dostępne w każdej sesji Gemini — jest tylko jeden config (`_greeting_config`), więc automatycznie
  dostępne zawsze
- Dopasowanie zadania po głosie: `_find_task()` — dokładne dopasowanie tekstu, potem substring
  (fuzzy, bo Igor nie zna wewnętrznych ID zadań)
- Ręczne akcje z przeglądarki (`ws_server.py`: `task_callbacks`, komenda tekstowa `TASK:<json>`)
  identyfikują zadania po `id` (precyzyjnie, bo UI zna id) — osobna ścieżka od głosowej (`handle_ws_command`)
- `ws_server.py`: nowy `connect_callbacks` — przy nowym połączeniu WS wysyła aktualną listę zadań
  (`task_tools.push_current_tasks`), żeby przeglądarka od razu widziała stan bez czekania na zmianę
- Zależność: ISSUE-023 done

## Test manualny

1. "Dodaj zadanie: kup mleko" → potwierdzenie głosem, zadanie na liście (log: `[TASKS] dodano`)
2. "Co mam do zrobienia?" → Gemini wymienia zadania
3. "Oznacz kup mleko jako zrobione" → status się zmienia (log: `[TASKS] oznaczono jako zrobione`)
4. "Usuń zadanie kup mleko" → znika z listy (log: `[TASKS] usunięto`) — potwierdzone, lista w
   przeglądarce zaktualizowała się na żywo
5. Restart brain → zadania nadal tam są (z Drive) — potwierdzone w ISSUE-023

---
applyTo: "**"
---

# Mordo — Lean Workflow (Solo Dev)

## Source of Truth

Na początku każdej sesji Claude Code czyta wyłącznie:
- `CURRENT_STATE.md` — aktualny stan projektu
- aktywny plik issue (`{issues}/ISSUE-NNN-*.md`) — definicja "gotowe"
- `project-config.md` — stack, fazy, ścieżki
- `team-context.md` — zasady współpracy

Wszystko inne czyta tylko gdy wprost potrzebne.

## Orientacja w projekcie

Na początku każdej sesji Claude Code czyta `CURRENT_STATE.md` w katalogu głównym.
**Przed zakończeniem każdej sesji** Claude Code MUSI zaktualizować `CURRENT_STATE.md` i `EPICS.md` i zcommitować — nawet jeśli Igor nie przypomni.
Przy zerwaniu sesji — powiedz "gdzie skończyliśmy" a Claude Code przeczyta plik i wróci do kontekstu.

```
pomysł / bug / zadanie
  → /discover (opcjonalnie — dla nowych pomysłów)
  → /plan (dla nietrywialnych zadań)
  → /dev (implementacja)
  → test manualny ("działa" / "nie działa + opis)
  → git push
  → aktualizacja docs jeśli potrzebne
```

## Stany issue

`planned` → `in-progress` → `done`

Pliki issue żyją w `{issues}/` przez cały cykl.
Po zamknięciu: zmień `status: done` w pliku. Nie przenoś. Zaktualizuj też `EPICS.md` (zaznacz `[x]`).

Każdy issue MUSI mieć sekcję `## Problemy i rozwiązania` — dopisuj na bieżąco gdy coś nie działa i jak to naprawiliśmy. To jest najcenniejsza wiedza, która ginie między sesjami.

**Epic** = kontener dla powiązanych issues. Żyje wyłącznie w `{issues}/EPICS.md` jako sekcja — bez osobnego pliku.
Zamykamy epic gdy wszystkie jego sub-issues są `done` (zmieniamy `[in-progress]` na `[done]` w EPICS.md).

## Limity dokumentów

**Żaden plik nie przekracza 230 linii.**
Dotyczy: SKILL.md, issue files, docs, kodu Python, firmware.
Przekroczenie = podziel na moduły przed kontynuacją.

## Zasady git

- Branch per issue: `feat/NNN-slug` od `main`
- Commit po każdym działającym kroku (nie czekaj na "gotowe")
- Push po teście manualnym
- Merge do `main` po "działa" od Igora

**Git: patrz `git-autonomy.md` — push automatycznie po przejętym teście.**

## Fazy — co wolno robić w danej fazie

Sprawdź `project-config.md` §Fazy projektu.
Nie implementuj funkcji z wyższej fazy zanim niższa nie jest stabilna.

## Agenci

Slash komendy to skrót, nie obowiązek. Możesz pisać naturalnie ("chcę żeby Mordo robił X") — Claude Code sam zdecyduje czy planować czy od razu implementować.

| Slash command | Kiedy użyć |
|---|---|
| `/discover` | nowy pomysł, nowa funkcja, "mam pomysł" |
| `/plan` | zadanie nieoczywiste: wiele plików, nowa integracja |
| `/dev` | implementacja |
| `/retro` | po zakończeniu fazy lub na życzenie |

## Backlog

Pomysły nie na teraz lądują w `{backlog}/`. Format: zwykła notatka, bez AC.
Claude Code zapisuje tam automatycznie gdy pomysł pada w trakcie sesji ale nie pasuje do aktualnej fazy.

## Konflikt / niejasność

STOP przed kodowaniem. Opisz sprzeczność, zaproponuj opcje, czekaj na wybór Igora.

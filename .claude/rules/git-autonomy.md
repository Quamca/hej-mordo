---
applyTo: "**"
---

# Git — Granice Autonomii

## Nigdy bez zgody Igora

- `git merge`
- `git checkout` (zmiana brancha)
- `git reset --hard`

## Wolno bez pytania

- `git status`
- `git diff`
- `git log`
- `git branch` (lista)
- `git add` (staging)
- `git commit` + `git push` — automatycznie po każdym teście manualnym który przeszedł

## Format commita

Z issue:
```
[ISSUE-NNN] typ: krótki opis

- zmiana 1
- zmiana 2
```

Bez issue (małe fixy, reguły, chore):
```
typ: krótki opis
```

Typy: `feat` `fix` `refactor` `chore` `docs`

## Zasada

Test manualny przechodzi → commit + push od razu, bez pytania.

## Konflikty między regułami — wersjonowanie

Gdy reguła się zmienia, dopisz na końcu pliku linię:
```
# Zmieniono: YYYYMMDDHHMI — co i dlaczego
```
Gdy jest konflikt między plikami reguł: plik z nowszą datą wygrywa.
Jeśli żaden nie ma daty — sprawdź `git log` na obu plikach i powiedz Igorowi który jest nowszy.

# Zmieniono: 202606261028 — git-autonomy jest nadrzędne; usunięto sprzeczne "nie commituj bez zgody" z team-context i workflow

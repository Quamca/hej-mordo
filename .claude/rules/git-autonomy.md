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


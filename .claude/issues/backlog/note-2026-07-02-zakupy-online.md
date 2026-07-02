---
title: "Automatyczne zakupy online (Allegro)"
type: note
faza: 4
created: 2026-07-02
---

## Pomysł

Mordo szuka i zamawia rzeczy w internecie na polecenie głosowe. Przykład z rozmowy: Igor mówi
"potrzebuję tabletek do zmywarki" → Mordo wchodzi na jego konto Allegro, sprawdza czy wcześniej
kupował taki produkt, jeśli tak — szuka tych samych tabletek w najtańszej aktualnej ofercie i
dodaje do koszyka.

Igor określił to wprost jako "daleka przyszłość" — nie planować teraz.

## Komponenty (wstępnie)

- Sterowanie przeglądarką / automatyzacja Allegro w imieniu Igora (logowanie, historia zakupów)
- Wyszukiwanie i porównywanie ofert tego samego produktu
- Dodawanie do koszyka (bez automatycznego finalizowania zakupu? — do ustalenia)

## Zależności

- Pasuje do Fazy 4 "PC Agenci" (`project-config.md`) — sterowanie komputerem/przeglądarką
- Powiązane: `product-vision.md` (roadmap), `note-2026-06-25-proaktywne-przypomnienia.md`

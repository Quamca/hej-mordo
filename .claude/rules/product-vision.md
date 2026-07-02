# Mordo — Wizja Produktu

Ten plik to żywa wizja, nie specyfikacja. Aktualizowany w miarę rozmów z Igorem — również poza tym
repo (np. z ChatGPT), gdy Igor uzna że warto to tu przenieść. Szczegóły behawioralne trafiają do
konkretnych issues (np. ISSUE-025) dopiero gdy są potwierdzone i gotowe do implementacji.

## Misja

Hej Mordo to inteligentny asystent, który widzi, słyszy i mówi (Gemini Flash Live). Nie jest tylko
wykonawcą poleceń — ma aktywnie pomagać Igorowi estymować, planować, dekomponować i realizować
zadania, które ma do zrobienia.

## Filozofia

Mordo ma czerpać z wiedzy o efektywnym zarządzaniu sobą w czasie, planowaniu, dekomponowaniu zadań
i motywowaniu. Konkretne źródła (książki) — do ustalenia, Igor wskaże które miał na myśli.

## Zachowanie — flow rozpoznania

Gdy Igor siada do komputera i Mordo go rozpoznaje, zagaduje:

> "Co robimy mordo? Masz nowe zadanie do zaplanowania, czy lecimy z tym co w kolejce?"

- Jeśli Igor ma coś nowego do zaplanowania → mówi, Mordo zapisuje.
- Jeśli nie → Mordo sprawdza listę i proponuje co jest ważne, pilne, lub małe (żeby zrobić od razu
  i mieć z głowy).

## Pętla feedbacku

Po każdym zadaniu Mordo analizuje: postęp, czas realizacji (rzeczywisty vs estymowany), oraz
satysfakcję Igora (z jego feedbackiem). Dokładne połączenie tych elementów jeszcze nie ustalone.

## Roadmap (szkic, nie zobowiązanie)

- **Teraz (EPIC-3)**: dostęp do Google Kalendarza/zadań — Mordo wie co tam jest, może dodawać nowe
  na podstawie tego co Igor powie.
- **Faza 3 "Proaktywny"**: integracja z mailem — Mordo sprawdza czy coś nie leży za długo, sam
  sugeruje zadania oraz kiedy i ile to zajmie. Powiązane: `{backlog}/note-2026-06-25-proaktywne-przypomnienia.md`
  (proaktywne zagadywanie po wykryciu twarzy, dopasowanie tonu do kontekstu).
- **Daleka przyszłość**: zakupy online — patrz `{backlog}/note-2026-07-02-zakupy-online.md`.

"""Function-calling do zarządzania zadaniami Igora głosem (Gemini Live tool calls) + komendy z przeglądarki."""
import json
import uuid

from google.genai import types
import tasks_store


def _push_update() -> None:
    from ws_server import enqueue_tasks
    enqueue_tasks(tasks_store.load_tasks())


def push_current_tasks() -> None:
    """Wywoływane przy nowym połączeniu WebSocket — wyślij aktualną listę od razu."""
    _push_update()

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="dodaj_zadanie",
        description="Dodaj nowe zadanie do listy Igora.",
        parametersJsonSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Treść zadania"},
                "estimate": {"type": "string", "description": "Szacowany czas, np. '2h' (opcjonalnie)"},
                "date": {"type": "string", "description": "Termin, np. '2026-07-05' (opcjonalnie)"},
            },
            "required": ["text"],
        },
    ),
    types.FunctionDeclaration(
        name="pokaz_zadania",
        description="Pokaż / przeczytaj aktualną listę zadań Igora.",
    ),
    types.FunctionDeclaration(
        name="edytuj_zadanie",
        description="Zmień treść, szacowany czas lub termin istniejącego zadania.",
        parametersJsonSchema={
            "type": "object",
            "properties": {
                "zadanie": {"type": "string", "description": "Jak Igor odnosi się do zadania (fragment treści)"},
                "nowa_tresc": {"type": "string", "description": "Nowa treść (opcjonalnie)"},
                "nowy_estimate": {"type": "string", "description": "Nowy szacowany czas (opcjonalnie)"},
                "nowa_data": {"type": "string", "description": "Nowy termin (opcjonalnie)"},
            },
            "required": ["zadanie"],
        },
    ),
    types.FunctionDeclaration(
        name="usun_zadanie",
        description="Usuń zadanie z listy.",
        parametersJsonSchema={
            "type": "object",
            "properties": {
                "zadanie": {"type": "string", "description": "Jak Igor odnosi się do zadania (fragment treści)"},
            },
            "required": ["zadanie"],
        },
    ),
    types.FunctionDeclaration(
        name="oznacz_zrobione",
        description="Oznacz zadanie jako zrobione.",
        parametersJsonSchema={
            "type": "object",
            "properties": {
                "zadanie": {"type": "string", "description": "Jak Igor odnosi się do zadania (fragment treści)"},
            },
            "required": ["zadanie"],
        },
    ),
]


def _find_task(tasks: list[dict], query: str) -> dict | None:
    query = query.lower().strip()
    for t in tasks:
        if t["text"].lower() == query:
            return t
    for t in tasks:
        if query in t["text"].lower() or t["text"].lower() in query:
            return t
    return None


def dodaj_zadanie(text: str, estimate: str | None = None, date: str | None = None) -> dict:
    tasks = tasks_store.load_tasks()
    task = {"id": uuid.uuid4().hex[:8], "text": text, "status": "todo", "estimate": estimate, "date": date}
    tasks.append(task)
    tasks_store.save_tasks(tasks)
    print(f"[TASKS] dodano: '{text}'", flush=True)
    _push_update()
    return {"ok": True, "zadanie": task}


def pokaz_zadania() -> dict:
    return {"zadania": tasks_store.load_tasks()}


def edytuj_zadanie(zadanie: str, nowa_tresc: str | None = None,
                    nowy_estimate: str | None = None, nowa_data: str | None = None) -> dict:
    tasks = tasks_store.load_tasks()
    task = _find_task(tasks, zadanie)
    if task is None:
        return {"ok": False, "blad": "nie znaleziono zadania"}
    if nowa_tresc:
        task["text"] = nowa_tresc
    if nowy_estimate:
        task["estimate"] = nowy_estimate
    if nowa_data:
        task["date"] = nowa_data
    tasks_store.save_tasks(tasks)
    print(f"[TASKS] edytowano: '{zadanie}'", flush=True)
    _push_update()
    return {"ok": True, "zadanie": task}


def usun_zadanie(zadanie: str) -> dict:
    tasks = tasks_store.load_tasks()
    task = _find_task(tasks, zadanie)
    if task is None:
        return {"ok": False, "blad": "nie znaleziono zadania"}
    tasks = [t for t in tasks if t["id"] != task["id"]]
    tasks_store.save_tasks(tasks)
    print(f"[TASKS] usunięto: '{zadanie}'", flush=True)
    _push_update()
    return {"ok": True}


def oznacz_zrobione(zadanie: str) -> dict:
    tasks = tasks_store.load_tasks()
    task = _find_task(tasks, zadanie)
    if task is None:
        return {"ok": False, "blad": "nie znaleziono zadania"}
    task["status"] = "done"
    tasks_store.save_tasks(tasks)
    print(f"[TASKS] oznaczono jako zrobione: '{zadanie}'", flush=True)
    _push_update()
    return {"ok": True, "zadanie": task}


HANDLERS = {
    "dodaj_zadanie": dodaj_zadanie,
    "pokaz_zadania": pokaz_zadania,
    "edytuj_zadanie": edytuj_zadanie,
    "usun_zadanie": usun_zadanie,
    "oznacz_zrobione": oznacz_zrobione,
}


def handle_ws_command(payload: str) -> None:
    """Ręczne akcje z przeglądarki (dodawanie/odhaczanie/edycja/usuwanie po id)."""
    try:
        cmd = json.loads(payload)
    except json.JSONDecodeError:
        return

    action = cmd.get("action")
    tasks = tasks_store.load_tasks()

    if action == "add" and cmd.get("text"):
        tasks.append({
            "id": uuid.uuid4().hex[:8], "text": cmd["text"],
            "status": "todo", "estimate": None, "date": None,
        })
    elif action == "toggle":
        for t in tasks:
            if t["id"] == cmd.get("id"):
                t["status"] = "todo" if t["status"] == "done" else "done"
                break
    elif action == "delete":
        tasks = [t for t in tasks if t["id"] != cmd.get("id")]
    elif action == "edit" and cmd.get("text"):
        for t in tasks:
            if t["id"] == cmd.get("id"):
                t["text"] = cmd["text"]
                break
    else:
        return

    tasks_store.save_tasks(tasks)
    _push_update()

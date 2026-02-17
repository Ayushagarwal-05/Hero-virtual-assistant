import json
import os

MEMORY_FILE = "hero_memory.json"


def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def set_fact(key, value):
    data = _load()
    data[key] = value
    _save(data)


def get_fact(key):
    return _load().get(key)


def delete_fact(key):
    data = _load()
    if key in data:
        del data[key]
        _save(data)


def list_facts():
    return _load()

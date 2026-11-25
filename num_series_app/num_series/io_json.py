import json
from datetime import datetime
from pathlib import Path

def save_series_json(data, path, meta=None):
    if not data:
        raise ValueError("Ряд пуст")
    values = []
    for x in data:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError(f"{x!r} не является числом")
        values.append(float(x))

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    payload = {"data": values}
    if meta is not None:
        meta = dict(meta)
        meta["n"] = len(values)
        meta["created"] = datetime.now().isoformat()
        payload["meta"] = meta
        
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

def load_series_json(path, with_meta=False):
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Файл не найден: {path}")
        
    try:
        content = path.read_text(encoding="utf-8")
        obj = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Файл не является корректным JSON")

    if isinstance(obj, list):
        data = obj
        meta = {}
    elif isinstance(obj, dict):
        if "data" not in obj:
            raise ValueError("В JSON нет поля 'data'")
        data = obj["data"]
        meta = obj.get("meta", {})
    else:
        raise ValueError("Неизвестная структура JSON")

    if not data:
        raise ValueError("Ряд пуст")

    result = []
    for x in data:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError(f"{x!r} не является числом")
        result.append(float(x))

    if with_meta:
        return result, meta
    return result
from pathlib import Path
from .io_json import load_series_json

def load_series_txt(path):
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Файл не найден: {path}")
    
    res = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            res.append(float(line))
        except ValueError:
            raise ValueError(f"{path}:{i}: не является числом")
            
    if not res:
        raise ValueError("Файл не содержит чисел")
    return res

def load_series_csv(path):
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Файл не найден: {path}")
        
    res = []
    lines = path.read_text(encoding="utf-8").splitlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        parts = line.replace(";", ",").split(",")
        if i == 1:
            try:
                [float(p) for p in parts if p.strip()]
            except ValueError:
                continue
                
        for p in parts:
            p = p.strip()
            if not p:
                continue
            try:
                res.append(float(p))
            except ValueError:
                raise ValueError(f"{path}:{i}: не является числом")
                
    if not res:
        raise ValueError("Файл не содержит чисел")
    return res

def load_series_auto(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_series_json(path)
    elif suffix == ".txt":
        return load_series_txt(path)
    elif suffix == ".csv":
        return load_series_csv(path)
    else:
        raise ValueError(f"Неизвестный формат: {suffix}")
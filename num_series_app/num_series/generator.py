import random
import math

def _validate_n(n) -> int:
    if isinstance(n, bool) or not isinstance(n, (int, float)):
        raise ValueError(f"{n!r} не является положительным целым: причина — неверный тип")
    if isinstance(n, float):
        if not n.is_integer():
            raise ValueError(f"{n!r} не является положительным целым: причина — не целое")
        n = int(n)
    if n <= 0:
        raise ValueError(f"{n!r} не является положительным целым: причина — <= 0")
    return n

def random_series(n, low=0.0, high=1.0, seed=None):
    n = _validate_n(n)
    if low >= high:
        raise ValueError("low должно быть меньше high")
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]

def sine_series(n, amplitude=1.0, frequency=0.1, noise=0.0, seed=None):
    n = _validate_n(n)
    rng = random.Random(seed)
    res = []
    for i in range(n):
        val = amplitude * math.sin(2 * math.pi * frequency * i)
        if noise > 0:
            val += rng.uniform(-noise, noise)
        res.append(val)
    return res

def trend_series(n, start=0.0, step=1.0, noise=0.0, seed=None):
    n = _validate_n(n)
    rng = random.Random(seed)
    res = []
    for i in range(n):
        val = start + step * i
        if noise > 0:
            val += rng.uniform(-noise, noise)
        res.append(val)
    return res
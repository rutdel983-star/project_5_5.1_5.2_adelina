def _check_empty(data):
    if not data:
        raise ValueError("Ряд пуст")

def mean(data):
    _check_empty(data)
    return sum(data) / len(data)

def median(data):
    _check_empty(data)
    s = sorted(data)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2.0
    return float(s[mid])

def spread(data):
    _check_empty(data)
    return max(data) - min(data)

def summarize(data):
    _check_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": min(data),
        "max": max(data),
    }
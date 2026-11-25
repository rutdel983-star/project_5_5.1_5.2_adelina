import time
from collections import deque

def _check_window(data, window):
    if not data:
        raise ValueError("Ряд пуст")
    if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
        raise ValueError("window должно быть целым положительным числом")
    if window > len(data):
        raise ValueError(f"window={window} больше длины ряда")
    return window

def simple_moving_average(data, window):
    w = _check_window(data, window)
    res = []
    running_sum = 0.0
    for i, x in enumerate(data):
        running_sum += x
        if i >= w:
            running_sum -= data[i - w]
        if i >= w - 1:
            res.append(running_sum / w)
    return res

def centered_moving_average(data, window):
    if window % 2 == 0:
        raise ValueError("window для CMA должно быть нечётным")
    w = _check_window(data, window)
    half = w // 2
    res = []
    for i in range(half, len(data) - half):
        res.append(sum(data[i - half : i + half + 1]) / w)
    return res

def exponential_moving_average(data, alpha):
    if not data:
        raise ValueError("Ряд пуст")
    if not (0 < alpha <= 1):
        raise ValueError("alpha должна быть в (0, 1]")
    res = [float(data[0])]
    for x in data[1:]:
        res.append(alpha * x + (1 - alpha) * res[-1])
    return res

def benchmark_moving_average(data, window, repeats=5):
    _check_window(data, window)
    
    def _benchmark_list():
        start = time.perf_counter()
        for _ in range(repeats):
            simple_moving_average(data, window)
        return time.perf_counter() - start

    def _benchmark_deque():
        start = time.perf_counter()
        for _ in range(repeats):
            dq = deque(maxlen=window)
            res = []
            running = 0.0
            for x in data:
                if len(dq) == window:
                    running -= dq[0]
                dq.append(x)
                running += x
                if len(dq) == window:
                    res.append(running / window)
        return time.perf_counter() - start

    return {
        "list": _benchmark_list(),
        "deque": _benchmark_deque()
    }
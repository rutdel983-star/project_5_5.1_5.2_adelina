from collections import deque

def simple_moving_average_deque(data, window):
    if not data:
        raise ValueError("Ряд пуст")
    if window > len(data):
        raise ValueError(f"window={window} больше длины ряда")
    
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
    return res

def centered_moving_average_deque(data, window):
    if window % 2 == 0:
        raise ValueError("window для CMA должно быть нечётного размера")
    if not data:
        raise ValueError("Ряд пуст")
    
    dq = deque(maxlen=window)
    res = []
    for x in data:
        dq.append(x)
        if len(dq) == window:
            res.append(sum(dq) / window)
    return res

def exponential_moving_average_deque(data, alpha):
    if not data:
        raise ValueError("Ряд пуст")
    if not (0 < alpha <= 1):
        raise ValueError("alpha должна быть в (0, 1]")
    
    dq = deque(maxlen=1)
    dq.append(float(data[0]))
    res = [dq[0]]
    for x in data[1:]:
        new_val = alpha * x + (1 - alpha) * dq[0]
        dq.clear()
        dq.append(new_val)
        res.append(new_val)
    return res
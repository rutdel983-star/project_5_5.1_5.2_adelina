import sys
import traceback
from num_series.generator import random_series, sine_series, trend_series, _validate_n
from num_series.stats import mean, median, spread, summarize
from num_series.moving_average import simple_moving_average, centered_moving_average, exponential_moving_average, benchmark_moving_average
from num_series.deque_average import simple_moving_average_deque, centered_moving_average_deque, exponential_moving_average_deque

RESULTS = []

def check(func):
    name = func.__name__
    try:
        func()
    except AssertionError as e:
        RESULTS.append((name, False, f"assert failed: {e}"))
    except Exception as e:
        RESULTS.append((name, False, f"{type(e).__name__}: {e}\n{traceback.format_exc()}"))
    else:
        RESULTS.append((name, True, ""))
    return func

def _raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type:
        return True
    except Exception as e:
        raise AssertionError(f"ожидалось {exc_type.__name__}, получено {type(e).__name__}")
    raise AssertionError(f"ожидалось {exc_type.__name__}, но исключения не было")

def approx_eq(a, b, eps=1e-9):
    if isinstance(a, list):
        assert len(a) == len(b), f"длины не равны: {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            assert abs(x - y) <= eps, f"[{i}]: {x} != {y}"
    else:
        assert abs(a - b) <= eps, f"{a} != {b}"

@check
def validate_n_ok():
    for n in (1, 5, 100):
        _validate_n(n)
    _validate_n(3.0)

@check
def validate_n_bad():
    for n in (0, -1, 3.5, "5", None):
        _raises(ValueError, _validate_n, n)

@check
def random_reproducible():
    assert random_series(20, seed=42) == random_series(20, seed=42)
    assert random_series(20, seed=1) != random_series(20, seed=2)

@check
def sine_amplitude():
    data = sine_series(100, amplitude=2.0, noise=0.0)
    assert all(-2.0 - 1e-9 <= x <= 2.0 + 1e-9 for x in data)

@check
def trend_linear():
    assert trend_series(5, start=0, step=2.0, noise=0.0) == [0.0, 2.0, 4.0, 6.0, 8.0]

@check
def stats_basic():
    approx_eq(mean([1, 2, 3]), 2.0)
    approx_eq(median([3, 1, 2]), 2.0)
    approx_eq(median([1, 2, 3, 4]), 2.5)
    assert spread([1, 2, 3]) == 2
    s = summarize([1, 2, 3, 4, 5])
    assert s["count"] == 5
    assert s["median"] == 3

@check
def stats_empty():
    for f in (mean, median, spread, summarize):
        _raises(ValueError, f, [])

@check
def sma_basic():
    approx_eq(simple_moving_average([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0])
    approx_eq(simple_moving_average([1, 2, 3], 3), [2.0])
    _raises(ValueError, simple_moving_average, [1, 2], 5)

@check
def cma_basic():
    approx_eq(centered_moving_average([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0])
    _raises(ValueError, centered_moving_average, [1, 2, 3, 4], 2)

@check
def ema_basic():
    approx_eq(exponential_moving_average([1.0, 2.0, 3.0], 0.5), [1.0, 1.5, 2.25])
    _raises(ValueError, exponential_moving_average, [1, 2, 3], 0.0)

@check
def deque_equivalent():
    data = list(range(50))
    for w in (1, 3, 7, 25):
        approx_eq(simple_moving_average_deque(data, w), simple_moving_average(data, w))
    approx_eq(centered_moving_average_deque(data, 5), centered_moving_average(data, 5))
    for alpha in (0.1, 0.5, 1.0):
        approx_eq(exponential_moving_average_deque(data, alpha), exponential_moving_average(data, alpha))

@check
def benchmark_shape():
    b = benchmark_moving_average(list(range(50)), window=5, repeats=2)
    assert set(b) == {"list", "deque"}
    assert b["list"] >= 0 and b["deque"] >= 0

def main() -> int:
    total = len(RESULTS)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, err in RESULTS:
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {name}")
        if not ok:
            print(f"        {err}")
    print(f"\nИтого: {passed}/{total} проверок пройдено")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
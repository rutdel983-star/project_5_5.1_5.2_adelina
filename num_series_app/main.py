import sys
import argparse
from num_series.stats import summarize
from num_series.generator import random_series, sine_series, trend_series
from num_series.moving_average import benchmark_moving_average, simple_moving_average, centered_moving_average, exponential_moving_average
from num_series.io_json import save_series_json
from num_series.io_file import load_series_auto

def main():
    parser = argparse.ArgumentParser(description="Алгоритмическая обработка числовых рядов")
    parser.add_argument("-n", type=int, default=10, help="Длина ряда")
    parser.add_argument("--seed", type=int, default=None, help="Seed генератора")
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="random", help="Тип ряда")
    parser.add_argument("--save", type=str, default=None, help="Сохранить в JSON")
    parser.add_argument("--load", type=str, default=None, help="Загрузить из файла")
    parser.add_argument("--window", type=int, default=5, help="Окно для скользящей средней")
    parser.add_argument("--benchmark", action="store_true", help="Запустить бенчмарк")
    
    args = parser.parse_args()

    try:
        # 1. Загрузка или генерация
        if args.load:
            data = load_series_auto(args.load)
        else:
            if args.kind == "random":
                data = random_series(args.n, seed=args.seed)
            elif args.kind == "sine":
                data = sine_series(args.n, seed=args.seed)
            else:
                data = trend_series(args.n, seed=args.seed)

        # 2. Сохранение (если указан флаг)
        if args.save:
            save_series_json(data, args.save)
            print(f"Сохранено {len(data)} значений в {args.save}")

        # 3. Статистика (вывод в консоль)
        stats = summarize(data)
        print(f"count={stats['count']} mean={stats['mean']:.4f} median={stats['median']:.4f}")

        # 4. Бенчмарк (если указан флаг)
        if args.benchmark:
            try:
                res = benchmark_moving_average(data, window=args.window, repeats=5)
                print(f"benchmark: list={res['list']:.6f}s deque={res['deque']:.6f}s")
            except ValueError as e:
                print(f"Ошибка бенчмарка: {e}", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
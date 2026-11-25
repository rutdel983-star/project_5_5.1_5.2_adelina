import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"

def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True, text=True, cwd=ROOT,
    )

class TestCLIBasics:
    def test_help_returns_zero(self):
        r = run_cli("--help")
        assert r.returncode == 0
        assert "usage" in r.stdout.lower()

    def test_default_run_returns_zero(self):
        r = run_cli("-n", "10", "--seed", "1")
        assert r.returncode == 0
        assert "count=" in r.stdout

    def test_kind_sine(self):
        r = run_cli("--kind", "sine", "-n", "15", "--seed", "7")
        assert r.returncode == 0

    def test_kind_trend(self):
        r = run_cli("--kind", "trend", "-n", "15", "--seed", "7")
        assert r.returncode == 0

    def test_invalid_kind_returns_nonzero(self):
        r = run_cli("--kind", "unknown", "-n", "5")
        assert r.returncode != 0
        assert "invalid choice" in r.stderr.lower() or "ошибка" in r.stderr.lower()

    def test_benchmark_flag(self):
        r = run_cli("-n", "20", "--seed", "1", "--window", "5", "--benchmark")
        assert r.returncode == 0
        assert "benchmark" in r.stdout.lower()

class TestCLIIO:
    def test_save_and_load_roundtrip(self, tmp_path):
        save_path = tmp_path / "series.json"
        r1 = run_cli("-n", "10", "--seed", "42", "--save", str(save_path))
        assert r1.returncode == 0
        assert save_path.exists()

        r2 = run_cli("--load", str(save_path), "--window", "3")
        assert r2.returncode == 0
        assert "count=10" in r2.stdout

    def test_load_missing_file_returns_one(self, tmp_path):
        r = run_cli("--load", str(tmp_path / "absent.json"))
        assert r.returncode == 1
        assert "ошибка" in r.stderr.lower()

    def test_error_message_goes_to_stderr(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        r = run_cli("--load", str(bad))
        assert r.returncode == 1
        assert r.stderr.strip() != ""
"""Summarize observed click-to-first-motion latency; never substitutes HTTP timings."""
import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


def read_samples(path):
    groups = defaultdict(list)
    blank = 0
    runs = set()
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"run", "poll_interval_s", "job", "latency_ms"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: missing CSV columns")
        for line, row in enumerate(reader, 2):
            try:
                run = int(row["run"])
                interval = float(row["poll_interval_s"])
                if run in runs or run < 1 or not math.isfinite(interval) or interval < 0:
                    raise ValueError("invalid/duplicate run or polling interval")
                runs.add(run)
                if not row["job"].strip():
                    raise ValueError("job is required")
                groups[interval]  # Keep unmeasured groups visible.
                if not row["latency_ms"].strip():
                    blank += 1
                    continue
                latency = float(row["latency_ms"])
                if not math.isfinite(latency) or latency < 0:
                    raise ValueError("latency must be finite and nonnegative")
                groups[interval].append(latency)
            except (ValueError, AttributeError, TypeError) as exc:
                raise ValueError(f"{path}:{line}: {exc}") from exc
    return dict(groups), blank


def report(label, groups):
    for interval, values in sorted(groups.items()):
        polls = f"{3600 / interval:.0f}" if interval else "—"
        if values:
            stats = f"{statistics.mean(values):.1f} | {min(values):.1f} | {max(values):.1f}"
        else:
            stats = "— | — | —"
        print(f"| {label} | {interval:g} | {len(values)}/30 | {stats} | {polls} |")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab2", type=Path)
    parser.add_argument("--lab1", type=Path)
    args = parser.parse_args()
    try:
        lab2, blanks = read_samples(args.lab2)
        baseline, baseline_blanks = read_samples(args.lab1) if args.lab1 else ({}, 0)
        if set(lab2) != {1.0, 5.0}:
            raise ValueError("Lab 2 must contain the 1 s and 5 s groups")
        if args.lab1 and set(baseline) != {0.0}:
            raise ValueError("Lab 1 uses interval 0 (direct, no polling)")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print("| Series | Poll interval (s) | Measured | Mean (ms) | Min (ms) | Max (ms) | Nominal polls/h |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    report("Lab 1 direct", baseline)
    report("Lab 2 post office", lab2)
    direct = baseline.get(0, [])
    if direct:
        for interval, values in sorted(lab2.items()):
            if values:
                delta = statistics.mean(values) - statistics.mean(direct)
                print(f"Lab 2 ({interval:g} s) minus Lab 1 mean: {delta:.1f} ms")
    complete = all(len(values) == 30 for values in lab2.values())
    complete = complete and (not args.lab1 or len(direct) == 30)
    print(f"Blank observations: {blanks + baseline_blanks}. "
          + ("Series complete." if complete else "INCOMPLETE: collect 30 observations per series."))


if __name__ == "__main__":
    main()

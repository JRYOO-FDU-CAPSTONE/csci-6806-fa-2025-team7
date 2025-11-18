import argparse
import csv
from pathlib import Path
import matplotlib.pyplot as plt

def load_dt_series(path: str, dt_col: str, x_col: str | None = None):
    xs = []
    ys = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        idx = 0
        for row in reader:
            if x_col is not None and x_col in row:
                try:
                    x_val = float(row[x_col])
                except ValueError:
                    continue
            else:
                x_val = idx
                idx += 1

            if dt_col not in row:
                raise KeyError(f"Column '{dt_col}' not found in CSV header")

            try:
                y_val = float(row[dt_col])
            except ValueError:
                continue

            xs.append(x_val)
            ys.append(y_val)

    if not xs:
        raise RuntimeError("No data points loaded; check column names.")
    return xs, ys

def main():
    parser = argparse.ArgumentParser(description="Generate DT figure")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--dt_col", required=True)
    parser.add_argument("--x_col", default=None)
    parser.add_argument("--out", default="figures/background_dt_example.png")
    args = parser.parse_args()

    xs, ys = load_dt_series(args.csv, args.dt_col, args.x_col)

    Path("figures").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(xs, ys)
    ax.set_xlabel("Request index" if args.x_col is None else args.x_col)
    ax.set_ylabel("DT (ms)")
    ax.set_title("Example DT over time")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(args.out, dpi=300)
    print(f"Saved DT figure to {args.out}")

if __name__ == "__main__":
    main()

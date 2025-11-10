import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd  

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RUN_DIR = PROJECT_ROOT / "runs" / "profile_memory"
LOG_FILE = RUN_DIR / "train_memory.log"
FIG_DIR = RUN_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLD_GB = 2.5 

if not LOG_FILE.exists():
    raise FileNotFoundError(
        f"Log file not found: {LOG_FILE}\n"
        "Run `./profile_memory.sh` first to generate it."
    )

peak_kb = None
pattern = re.compile(r"Maximum resident set size \(kbytes\):\s+(\d+)")

with LOG_FILE.open() as f:
    for line in f:
        m = pattern.search(line)
        if m:
            peak_kb = int(m.group(1))
            break

if peak_kb is None:
    raise RuntimeError(
        f"Could not find 'Maximum resident set size (kbytes)' in {LOG_FILE}"
    )

peak_gb = peak_kb / (1024 ** 2)

print(f"Log file       : {LOG_FILE}")
print(f"Peak RSS (KB)  : {peak_kb:,}")
print(f"Peak memory GB : {peak_gb:.3f} GB")
print(f"Expected       : Peak memory < {THRESHOLD_GB} GB")

passed = peak_gb < THRESHOLD_GB
if passed:
    print("[RESULT] PASS: memory usage is below threshold.")
else:
    print("[RESULT] FAIL: memory usage exceeds threshold.")

labels = ["Peak usage", "Limit"]
values = [peak_gb, THRESHOLD_GB]

peak_color = "tab:green" if passed else "tab:red"
colors = [peak_color, "tab:gray"]

fig, ax = plt.subplots(figsize=(6, 4))

bars = ax.bar(labels, values, color=colors, width=0.55)

for bar, val in zip(bars, values):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.05,
        f"{val:.2f} GB",
        ha="center",
        va="bottom",
        fontsize=11,
    )

y_max = max(values) * 1.25
ax.set_ylim(0, y_max)

ax.set_ylabel("Memory usage (GB)", fontsize=13)
ax.set_title("Baleen training memory usage", fontsize=14)

ax.grid(axis="y", linestyle="--", alpha=0.6)

fig.tight_layout()
out_path = FIG_DIR / "profile_memory.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)

print(f"[FIGURE] Saved memory plot to: {out_path}")

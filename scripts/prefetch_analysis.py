#!/usr/bin/env python3
"""
Prefetch policy analysis (Nas) — parses JSONLZ logs and makes figures.
Inputs:
  runs/prefetch/{never_128,always_128,rejectfirst_128}/rejectx-ap-1_0.508154_lru_128GB/full_0_0.1_cache_perf.txt.lzma
Outputs:
  runs/prefetch/figures/prefetch_hit_rate.png
  runs/prefetch/figures/prefetch_flash_write_rate.png
  runs/prefetch/figures/prefetch_summary.csv
"""

import os, lzma, json, csv
from pathlib import Path
import matplotlib.pyplot as plt

root = Path("runs/prefetch")
pairs = [
    ("never",       root/"never_128"/"rejectx-ap-1_0.508154_lru_128GB"/"full_0_0.1_cache_perf.txt.lzma"),
    ("always",      root/"always_128"/"rejectx-ap-1_0.508154_lru_128GB"/"full_0_0.1_cache_perf.txt.lzma"),
    ("rejectfirst", root/"rejectfirst_128"/"rejectx-ap-1_0.508154_lru_128GB"/"full_0_0.1_cache_perf.txt.lzma"),
]

def read_json_lz(path: Path):
    with lzma.open(path, "rb") as f:
        data = f.read().decode("utf-8", "ignore")
    # Some logs are pretty-printed JSON; load once.
    return json.loads(data)

def safe_get(d, key, default=None):
    return d.get("results", {}).get(key, default)

rows = []
for policy, fp in pairs:
    if not fp.exists():
        print(f"[WARN] Missing file for {policy}: {fp}")
        continue
    obj = read_json_lz(fp)

    hit = safe_get(obj, "FlashCacheHitRate", 0.0)
    fw  = safe_get(obj, "FlashWriteRate", 0.0)
    cbw = safe_get(obj, "ClientBandwidth", 0.0)
    tchw = safe_get(obj, "TotalChunkWritten", 0)

    rows.append({
        "policy": policy,
        "FlashCacheHitRate": float(hit) if hit is not None else 0.0,
        "FlashWriteRate": float(fw) if fw is not None else 0.0,
        "ClientBandwidth": float(cbw) if cbw is not None else 0.0,
        "TotalChunkWritten": int(tchw) if tchw is not None else 0,
    })

# Ensure deterministic order: never, always, rejectfirst
order = {"never":0, "always":1, "rejectfirst":2}
rows.sort(key=lambda r: order.get(r["policy"], 99))

# Write CSV summary
figdir = root/"figures"
figdir.mkdir(parents=True, exist_ok=True)
csv_path = figdir/"prefetch_summary.csv"
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["policy","FlashCacheHitRate","FlashWriteRate","ClientBandwidth","TotalChunkWritten"])
    w.writeheader()
    w.writerows(rows)

# Bar chart: Hit Rate
labels = [r["policy"] for r in rows]
hr_vals = [r["FlashCacheHitRate"] for r in rows]

plt.figure()
plt.title("Flash Cache Hit Rate by Prefetch Policy", fontsize=14)
plt.ylabel("Hit Rate", fontsize=12)
plt.xlabel("Policy", fontsize=12)
plt.bar(labels, hr_vals)
for i, v in enumerate(hr_vals):
    plt.text(i, v + 0.01, f"{v:.2f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(figdir/"prefetch_hit_rate.png", dpi=200)
plt.close()

# Bar chart: Flash Write Rate
fw_vals = [r["FlashWriteRate"] for r in rows]

plt.figure()
plt.title("Flash Write Rate by Prefetch Policy", fontsize=14)
plt.ylabel("Write Rate (MB/s)", fontsize=12)
plt.xlabel("Policy", fontsize=12)
plt.bar(labels, fw_vals)
for i, v in enumerate(fw_vals):
    plt.text(i, v + 0.5, f"{v:.2f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(figdir/"prefetch_flash_write_rate.png", dpi=200)
plt.close()

print(f"[OK] Wrote: {csv_path}")
print(f"[OK] Wrote: {figdir/'prefetch_hit_rate.png'}")
print(f"[OK] Wrote: {figdir/'prefetch_flash_write_rate.png'}")

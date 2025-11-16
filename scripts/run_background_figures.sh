#!/usr/bin/env bash
set -e

python scripts/background_dt_from_csv.py \
  --csv results/results_release.csv \
  --dt_col "Mean Time In System (s)" \
  --out figures/background_dt_example.png

python scripts/background_episodes_plot.py \
  --out figures/background_episodes_example.png

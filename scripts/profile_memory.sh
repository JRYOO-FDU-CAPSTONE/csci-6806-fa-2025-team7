#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

OUT_DIR="$PROJECT_ROOT/runs/profile_memory"
LOG_FILE="$OUT_DIR/train_memory.log"

mkdir -p "$OUT_DIR"

echo "[profile_memory] Output dir: $OUT_DIR"
echo "[profile_memory] Log file   : $LOG_FILE"
echo "[profile_memory] Running small_test training under /usr/bin/time -v ..."

rm -f "$LOG_FILE"

/usr/bin/time -v \
  "$PROJECT_ROOT/BCacheSim/run_py.sh" py -B -m BCacheSim.episodic_analysis.train \
    --exp small_test \
    --policy PolicyUtilityServiceTimeSize2 \
    --region Region1 \
    --sample-ratio 0.1 \
    --sample-start 0 \
    --trace-group 201910 \
    --supplied-ea physical \
    --target-wrs 50 100 \
    --target-csizes 366.475 \
    --output-base-dir "$OUT_DIR" \
    --eviction-age 5892.856 \
    --rl-init-kwargs filter_=prefetch \
    --train-target-wr 35.599 \
    --train-models admit \
    --train-split-secs-start 0 \
    --train-split-secs-end 1200 \
    --ap-acc-cutoff 15 \
    --ap-feat-subset meta+block+chunk \
  2> "$LOG_FILE"

echo "[profile_memory] Done. /usr/bin/time -v output saved to:"
echo "  $LOG_FILE"

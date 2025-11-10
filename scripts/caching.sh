#!/bin/bash
# Small admission training (quick run for A/B plots)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# Activate venv
source "$PROJECT_ROOT/.venv/bin/activate"

# Run training (writes under runs/small_test)
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
  --output-base-dir "$PROJECT_ROOT/runs/small_test" \
  --eviction-age 5892.856 \
  --rl-init-kwargs filter_=prefetch \
  --train-target-wr 35.599 \
  --train-models admit \
  --train-split-secs-start 0 \
  --train-split-secs-end 1200 \
  --ap-acc-cutoff 15 \
  --ap-feat-subset meta+block+chunk

echo "✅ small_test admission training complete. Outputs in runs/small_test/"

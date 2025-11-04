#!/bin/bash

# Path for the directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# Run the Baleen training command (it is small test)
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

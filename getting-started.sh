#!/usr/bin/env bash
set -euo pipefail

# You should start this script from the Baleen-FAST24 repo root
if [ ! -d "BCacheSim" ]; then
  echo "Please run this from the Baleen-FAST24 repo root (BCacheSim/ should exist here)."
  exit 1
fi

echo "In Baleen-FAST24: $(pwd)"

# --- Choose ONE env method: Conda (recommended) OR pip/venv ---

USE_CONDA=1   # set to 0 to use Python venv + pip

if [ "$USE_CONDA" -eq 1 ]; then
  # --- Conda path ---
  # If you don't already have conda, install Miniconda (one-time)
  if ! command -v conda >/dev/null 2>&1; then
    echo "Conda not found; installing Miniconda..."
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
  else
    echo "Conda found."
    eval "$(conda shell.bash hook)"
  fi

  echo "Creating/Updating env cachelib-py-3.11..."
  conda env create -f BCacheSim/install/env_cachelib-py-3.11.yaml || conda env update -f BCacheSim/install/env_cachelib-py-3.11.yaml
  conda activate cachelib-py-3.11

  # (optional) extra pip deps if needed
  python -m pip install -r BCacheSim/install/requirements.txt || true

else
  # --- Python venv + pip path ---
  echo "Using python venv + pip..."
  sudo apt -y update && sudo apt -y install python3-venv
  python3 -m venv ~/.venvs/cachelib
  source ~/.venvs/cachelib/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -r BCacheSim/install/requirements.txt
fi

# --- Download traces (skips if already present) ---
cd data
if [ ! -d tectonic ]; then
  echo "Downloading tectonic traces..."
  bash get-tectonic.sh || echo "Trace download failed/was skipped. You can retry later."
else
  echo "Traces already present; skipping download."
fi
cd ..

# --- Quick baseline (RejectX) ---
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/example/rejectx/config.json

# --- Train Baleen (short) ---
./BCacheSim/run_py.sh py -B -m BCacheSim.episodic_analysis.train --exp example --policy PolicyUtilityServiceTimeSize2 --region Region1 --sample-ratio 0.1 --sample-start 0 --trace-group 201910 --supplied-ea physical --target-wrs 34 50 100 75 20 10 60 90 30 --target-csizes 366.475 --output-base-dir runs/example/baleen --eviction-age 5892.856 --rl-init-kwargs filter_=prefetch --train-target-wr 35.599 --train-models admit prefetch --train-split-secs-start 0 --train-split-secs-end 86400 --ap-acc-cutoff 15 --ap-feat-subset meta+block+chunk

# --- Run Baleen ---
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/example/baleen/prefetch_ml-on-partial-hit/config.json

echo "✅ Done. Open notebooks/example/example.ipynb to inspect results."

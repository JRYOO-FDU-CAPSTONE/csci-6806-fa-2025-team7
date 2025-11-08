

#!/usr/bin/env bash
# Prefetch Policy Experiments — Nas
# Runs three variants (never, always, rejectfirst) at 128 GB with RejectX AP.

set -euo pipefail

TRACE="data/tectonic/201910/Region1/full_0_0.1.trace"
SIZE=128

AP_FLAGS="--ap rejectx --rejectx-ap --ap-threshold 1.0 --ap-probability 0.508154"

run_case () {
  local PREFETCH_MODE="$1"   # never | always | rejectfirst
  local OUTDIR="runs/prefetch/${PREFETCH_MODE}_${SIZE}"

  echo ">>> Running prefetch=${PREFETCH_MODE}, size=${SIZE}GB ..."
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    -t "${TRACE}" \
    --eviction-policy LRU \
    -s "${SIZE}" \
    ${AP_FLAGS} \
    --prefetch-when "${PREFETCH_MODE}" \
    -o "${OUTDIR}" \
    --ignore-existing

  echo ">>> Output: ${OUTDIR}"
  echo
}

mkdir -p runs/prefetch

# 1) No Prefetch
run_case "never"

# 2) Always Prefetch
run_case "always"

# 3) Prefetch after reject (reject-first)
run_case "rejectfirst"

echo "All prefetch experiments finished."




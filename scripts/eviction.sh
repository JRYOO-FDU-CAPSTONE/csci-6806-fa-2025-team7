
# Eviction policy experiment - configurable region

PYTHON=py
REGION="Region2"
EXP_NAME="small_test_evict_${REGION,,}" 

ARGS="-B -m BCacheSim.episodic_analysis.train \
  --exp $EXP_NAME \
  --policy PolicyUtilityServiceTimeSize2 \
  --region $REGION \
  --sample-ratio 0.1 \
  --sample-start 0 \
  --trace-group 201910 \
  --supplied-ea physical \
  --target-wrs 50 100 \
  --target-csizes 366.475 \
  --output-base-dir $(dirname $(realpath $0))/../runs/$EXP_NAME \
  --eviction-age 5892.856 \
  --rl-init-kwargs filter_=prefetch \
  --train-target-wr 35.599 \
  --train-models evict \
  --train-split-secs-start 0 \
  --train-split-secs-end 1200 \
  --ap-acc-cutoff 15 \
  --ap-feat-subset meta+block+chunk"

case "$PYTHON" in
    py) PYTHON_BIN=python ;;
    python*) PYTHON_BIN=$PYTHON ;;
    *) PYTHON_BIN=python ;;
esac

cd $(dirname $(realpath $0))/../BCacheSim/..
stdbuf -eL -oL $PYTHON_BIN $ARGS

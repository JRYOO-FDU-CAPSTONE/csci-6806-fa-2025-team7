# Artifact for Baleen (FAST 2024)

_Baleen: ML Admission & Prefetching for Flash Caches_

_[Paper (Preprint)](https://wonglkd.fi-de.net/papers/Baleen-FAST24.pdf) | [Code](https://github.com/wonglkd/BCacheSim/) | [Data](https://ftp.pdl.cmu.edu/pub/datasets/Baleen24/) | [Video walkthrough](https://www.tiny.cc/BaleenArtifactYT) | [Reproduce on Chameleon](https://www.chameleoncloud.org/experiment/share/aa6fb454-6452-4fc8-994a-b028bfc3c82d)_ 

This repository is targeted at those seeking to reproduce the results found in the Baleen paper and contains a frozen copy of the code.  
If you are looking to use Baleen, please go to https://github.com/wonglkd/BCacheSim/ for the latest version.

![Artifact Available](https://sysartifacts.github.io/images/usenix_available.svg)
![Artifact Functional](https://sysartifacts.github.io/images/usenix_functional.svg)
![Results Reproduced](https://sysartifacts.github.io/images/usenix_reproduced.svg)

---

## SYSTEM REQUIREMENTS
```
OS:Ubuntu 22.04 LTS (tested)  
CPU: x86_64 with AVX2 support  
RAM: ≥ 8 GB  
GPU: Optional (for PyTorch acceleration)  
Python: 3.10.6  
Dependencies:
    numpy==1.23.5  
    matplotlib==3.7.1  
    torch==2.1.0  
    pandas==2.2.2  
```

## Getting Started

_Time estimate: 60 mins (20 mins interactive)._

## Installation (using pip)

To set up Baleen locally with pip, follow these steps:

```bash
# 1. Clone the repository
git clone --recurse-submodules https://github.com/wonglkd/Baleen-FAST24.git
cd Baleen-FAST24

# 2. Create and activate a virtual environment
python3 -m venv baleen-env
source baleen-env/bin/activate

# 3. Upgrade pip and install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r BCacheSim/install/requirements.txt

# 4. Download trace files
cd data
bash get-tectonic.sh
cd ..
```

---

## Reproducing Results

To reproduce the main experimental results from the Baleen paper, run the following commands:

```bash
# Caching
python3 scripts/caching_policy.py

# Eviction
python3 scripts/eviction_analysis.py

# Admission
python3 scripts/addmission_plot_figures.py

# Prefetch
python3 scripts/prefetch_analysis.py

# Memory Profile
python3 scripts/profile_memory.py
```

---

## Validation Checklist to generate results
For run the policy we have already created Bash files.
Go to the `scripts` folder
```cd scripts```. you will find all the results in `/runs` folder with each policy name folder and with their csv files.
``` 
Test-1
# Caching
./caching_policy.sh  

Test-2
# Eviction
./eviction_analysis.sh
 
Test-3
# Admission
./addmission_plot_figures.sh

Test-4
# Prefetch
./prefetch_analysis.sh

Test-5
# Memory Profile
./profile_memory.sh

 
```
---

## Detailed Instructions

This section assumes you have completed the 'Getting Started' section and have installed the code and downloaded the traces.

As it requires too much computation time to rerun every single experiment,  
we suggest the following steps to maximize the use of reviewers' time in evaluating our paper.  
We supply our traces, code, and intermediate results from our experimental runs.

**Roadmap for evaluation:**  
1. Test out Baleen's ML training & simulator (in Getting Started).  
   - What: simulate RejectX baseline, train Baleen models, simulate Baleen  
   - Expected results: notebooks/example/example.ipynb  
2. To check any of the individual policy:
     - You will find scripts folder in the root repo in that all the bash files along with their python file like if you want to generate the figures with the help of matplotlib library.
3. If you find error:   
    - please download the all requirements to run that specific policy.

---

## Directory structure

data — traces used as input  
runs — where experiment results are stored  
tmp — temporary directory for ML models and generated episode files  
scripts — where all the scripts and bash files are stores to run the policies

---

## Limitations

- The multiple parallelism with simultaneous background region analysis is not enabled; the current implementation is single-threaded.  
- Eviction and admission scripts depend on static `config.json` files that must be manually updated between runs.  
- Prefetch policy results are sensitive to the trace sampling ratio; no adaptive sampling mechanism is implemented.  
- Aggregated CSV logs are used to compute cache hit rate metrics — no real-time performance monitoring.  
- The system assumes Tectonic traces already exist; missing trace regeneration is unsupported.  
- ML-based admission and prefetch policies are trained with fixed model weights; retraining or fine-tuning on new workloads is not yet supported.  

---

## Additional notes

624 machine-days were used for the final runs to generate the results used in the paper.  
Each simulation of a ML policy takes at least 30 minutes, multiplied by 7 traces and 10 samples each.

---

## Future research

`notebooks/reproduce/exps-cluster-sample.ipynb` will be useful to run experiments efficiently but requires more dependencies (brooce, redis).

---

## Troubleshooting

If you face any issues, please try:
```
1. Ensure you have the latest repository:  
git pull --recurse-submodules  

2. Refresh the dataset:  
cd data  
bash clean.sh  
bash get-tectonic.sh  

3. For Chameleon Cloud issues, contact their helpdesk: help@chameleoncloud.org
```
---

## Any questions?

Please open a GitHub issue: https://github.com/wonglkd/Baleen-FAST24/issues/new  
or email the authors (see https://wonglkd.fi-de.net)

---

## Reference
```
**[Baleen: ML Admission & Prefetching for Flash Caches](https://www.usenix.org/conference/fast24/presentation/wong)**  
Daniel Lin-Kit Wong, Hao Wu, Carson Molder, Sathya Gunasekar, Jimmy Lu, Snehal Khandkar, Abhinav Sharma, Daniel S. Berger, Nathan Beckmann, Gregory R. Ganger  
_USENIX FAST 2024_
```

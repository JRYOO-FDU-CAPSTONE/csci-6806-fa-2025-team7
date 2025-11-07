import argparse
import os
import re
import json
import sys
import subprocess
from pathlib import Path
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt

def paths():
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    return {
        "root": root,
        "bcache_root": root / "BCacheSim",
        "config_rejectx": root / "runs" / "example" / "rejectx" / "config.json",
        "figs_root": root / "figs",
        "rejectx_root": root / "runs" / "example" / "rejectx",
        "data_root": root / "data" / "tectonic",
    }

def ensure(p: Path, what: str):
    if not p.exists():
        raise FileNotFoundError(f"{what} not found: {p}")

def parse_args():
    ap = argparse.ArgumentParser(description="Run RejectX caching and produce plots.")
    ap.add_argument("--group", default="20230325", help="Trace group: 201910 | 202110 | 20230325")
    ap.add_argument("--region", default="Region5", help="Region name, e.g., Region5")
    ap.add_argument("--trace-file", default="full_0_0.1.trace", help="Trace file in region dir")
    ap.add_argument("--ap-threshold", type=float, default=0.5)
    ap.add_argument("--ap-probability", type=float, default=0.5)
    ap.add_argument("--out-prefix", default="cache", help="figs/{prefix}_{region}")
    ap.add_argument("--plot-only", action="store_true", help="Skip running; only make plots from latest output")
    ap.add_argument("--skip-plots", action="store_true", help="Run sim but do not generate plots")
    return ap.parse_args()

def newest_rejectx_run_dir(rejectx_root: Path) -> Path | None:
    run_dirs = sorted(
        (Path(p) for p in glob(str(rejectx_root / "rejectx-ap-*"))),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return run_dirs[0] if run_dirs else None

def discover_perf_files(run_dir: Path):
    perf_txt = run_dir / "full_0_0.1_cache_perf.txt"
    stats_json = run_dir / "full_0_0.1.stats.json"
    if not perf_txt.exists():
        txt_candidates = list(run_dir.glob("*cache_perf*.txt"))
        if txt_candidates:
            perf_txt = txt_candidates[0]
    if not stats_json.exists():
        js_candidates = list(run_dir.glob("*.stats.json"))
        if js_candidates:
            stats_json = js_candidates[0]
    return perf_txt if perf_txt.exists() else None, stats_json if stats_json.exists() else None

def _to_number(v):
    try:
        if isinstance(v, (int, float)):
            return float(v)
        s = str(v)
        s = re.sub(r"[,%]", "", s).strip()
        return float(s)
    except Exception:
        return v

def parse_cache_perf(perf_txt: Path) -> pd.Series:
    try:
        df = pd.read_csv(perf_txt, sep=r"[,\t]+|\s{2,}", engine="python")
        if len(df) >= 1 and df.shape[1] > 1:
            s = df.iloc[0].copy()
            s.index = [c.strip() for c in s.index]
            return s.apply(_to_number)
    except Exception:
        pass
    d = {}
    with perf_txt.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
            elif "=" in line:
                k, v = line.split("=", 1)
            else:
                parts = re.split(r"\s{2,}", line)
                if len(parts) >= 2:
                    k, v = parts[0], parts[1]
                else:
                    continue
            d[k.strip()] = _to_number(v.strip())
    if not d:
        raise ValueError(f"Could not parse metrics from {perf_txt}")
    return pd.Series(d)

def parse_stats(stats_json: Path) -> dict | None:
    try:
        with stats_json.open("r") as f:
            return json.load(f)
    except Exception:
        return None

def plot_metrics_bar(series: pd.Series, title: str, out_path: Path):
    aliases = {
        "HitRate": ["HitRate", "Cache Hit Rate", "hit_rate"],
        "MissRate": ["MissRate", "miss_rate"],
        "PeakDiskTime": ["PeakDiskTime", "Peak DT", "peak_dt", "PeakDisk-head Time"],
        "BackendWriteMBps": ["BackendWriteMBps", "Write MBps", "backend_write_mbps"],
        "AvgLatency": ["AvgLatency", "Latency", "AverageLatency", "avg_latency_ms"],
        "IOPSSavedRatio": ["IOPSSavedRatio", "IOPS Saved Ratio", "iops_saved_ratio"],
        "ServiceTimeSavedRatio": ["Service Time Saved Ratio", "service_time_saved_ratio"],
    }
    metrics = {}
    for canon, keys in aliases.items():
        for k in keys:
            if k in series.index:
                try:
                    metrics[canon] = float(series[k])
                    break
                except Exception:
                    continue
    if not metrics:
        print("No recognizable numeric metrics for bar plot; skipping.")
        return
    s = pd.Series(metrics)
    plt.figure(figsize=(8, 5))
    ax = s.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title(title, fontsize=10, fontweight="bold", pad=8)
    plt.ylabel("Value", fontsize=10, fontweight="bold")
    plt.xticks(rotation=25, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=10, label_type="edge")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def plot_stats_timeseries(stats: dict, out_dir: Path):
    if not isinstance(stats, dict):
        return
    def _plot(key, ylabel, fname):
        arr = stats.get(key)
        if not isinstance(arr, list) or not arr:
            return
        plt.figure(figsize=(8, 4.5))
        plt.plot(range(len(arr)), arr, marker="o", linewidth=1.8, markersize=4)
        plt.xlabel("Interval", fontsize=10, fontweight="bold")
        plt.ylabel(ylabel, fontsize=10, fontweight="bold")
        plt.title(f"{ylabel} over Simulation Intervals", fontsize=10, fontweight="bold", pad=8)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        outp = out_dir / fname
        plt.savefig(outp, dpi=300)
        plt.close()
        print(f"Saved: {outp}")
    _plot("hit_rate", "Hit Rate", "timeseries_hit_rate.png")
    _plot("miss_rate", "Miss Rate", "timeseries_miss_rate.png")
    _plot("backend_write_mbps", "Backend Write (MB/s)", "timeseries_backend_write.png")
    _plot("avg_latency_ms", "Avg Latency (ms)", "timeseries_avg_latency.png")

def run_sim_and_get_output_dir(cmd, cwd: Path) -> Path | None:
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    print(stdout, end="")
    if proc.returncode != 0:
        print(stderr)
        raise SystemExit(proc.returncode)
    m = re.search(r"Output dir:\s*(.+)", stdout)
    if m:
        out_rel = m.group(1).strip()
        out_path = (cwd / out_rel).resolve()
        if out_path.exists():
            return out_path
    p = paths()
    fallback = newest_rejectx_run_dir(p["rejectx_root"])
    return fallback

def main():
    p = paths()
    args = parse_args()
    ensure(p["bcache_root"], "BCacheSim directory")
    ensure(p["config_rejectx"], "RejectX config")
    trace_path = p["data_root"] / args.group / args.region / args.trace_file
    ensure(trace_path, "Trace file")
    region_tag = args.region.lower()
    figs_dir = p["figs_root"] / f"{args.out_prefix}_{region_tag}" / "plots"
    figs_dir.mkdir(parents=True, exist_ok=True)
    run_dir = None
    if not args.plot_only:
        cmd = [
            sys.executable, "-m", "BCacheSim.cachesim.simulate_ap",
            "-t", str(trace_path),
            "-o", str(p["figs_root"] / f"{args.out_prefix}_{region_tag}"),
            "--config", str(p["config_rejectx"]),
            "--rejectx-ap",
            "--ap-threshold", str(args.ap_threshold),
            "--ap-probability", str(args.ap_probability),
        ]
        print("🚀 Running RejectX caching")
        print(f"   Group  : {args.group}")
        print(f"   Region : {args.region}")
        print(f"   Trace  : {trace_path}")
        print(f"   Figs   : {figs_dir.parent}")
        run_dir = run_sim_and_get_output_dir(cmd, p["root"])
        if run_dir:
            print(f"Detected run dir: {run_dir}")
        else:
            print("Could not detect run dir from stdout; will use newest rejectx run.")
    if run_dir is None:
        run_dir = newest_rejectx_run_dir(p["rejectx_root"])
        if not run_dir:
            raise SystemExit(f"No rejectx runs found in {p['rejectx_root']}")
    perf_txt, stats_json = discover_perf_files(run_dir)
    print(f"Using results from: {run_dir}")
    if perf_txt:
        print(f"Perf file: {perf_txt}")
    if stats_json:
        print(f"Stats JSON: {stats_json}")
    if args.skip_plots:
        print("skip-plots requested; exiting.")
        return
    summary_csv = p["rejectx_root"] / f"summary_{region_tag}.csv"
    series = None
    if perf_txt:
        try:
            series = parse_cache_perf(perf_txt)
        except Exception as e:
            print(f"Could not parse {perf_txt}: {e}")
    if isinstance(series, pd.Series):
        row = series.to_frame().T
        if summary_csv.exists():
            prev = pd.read_csv(summary_csv)
            pd.concat([prev, row], ignore_index=True).to_csv(summary_csv, index=False)
        else:
            row.to_csv(summary_csv, index=False)
        print(f"Wrote summary CSV: {summary_csv}")
        plot_metrics_bar(series, f"RejectX — Key Metrics ({args.region})", figs_dir / "metrics_bar.png")
    stats_obj = parse_stats(stats_json) if stats_json else None
    if stats_obj:
        plot_stats_timeseries(stats_obj, figs_dir)
    print(f"All figures (if generated) are in: {figs_dir.resolve()}")

if __name__ == "__main__":
    main()

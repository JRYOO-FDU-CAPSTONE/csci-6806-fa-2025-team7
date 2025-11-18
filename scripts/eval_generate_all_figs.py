import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    # Load CSV
    df = pd.read_csv("results/results_release.csv")

    out_dir = Path("figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Use row index as a simple x-axis (each row = one experiment/config/region)
    x = range(len(df))

    # ---------- Figure 3: DT across experiments ----------
    try:
        dt = df["Mean Time In System (s)"]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, dt)
        ax.set_xlabel("Experiment index")
        ax.set_ylabel("Mean Time In System (s)")
        ax.set_title("DT behaviour across experiments")
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig3_dt_across_experiments.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 3: DT across experiments")
    except KeyError:
        print("Column 'Mean Time In System (s)' not found for Figure 3")

    # ---------- Figure 4: Eviction age distribution ----------
    try:
        ev_age = df["Avg Eviction Age (s)"].dropna()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(ev_age, bins=30)
        ax.set_xlabel("Avg Eviction Age (s)")
        ax.set_ylabel("Count")
        ax.set_title("Distribution of eviction age")
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig4_eviction_age_hist.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 4: Eviction age distribution")
    except KeyError:
        print("Column 'Avg Eviction Age (s)' not found for Figure 4")

    # ---------- Figure 5: Hit rate across experiments ----------
    try:
        hit_rate = df["Hit Rate (Hz)"]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, hit_rate)
        ax.set_xlabel("Experiment index")
        ax.set_ylabel("Hit Rate (Hz)")
        ax.set_title("Hit rate across experiments")
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig5_hit_rate.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 5: Hit rate across experiments")
    except KeyError:
        print("Column 'Hit Rate (Hz)' not found for Figure 5")

    # ---------- Figure 6: Successful vs wasted prefetches ----------
    try:
        useful = df["TotalUsefulPrefetches"]
        wasted = df["TotalWastedPrefetches"]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, useful, label="Useful prefetches")
        ax.plot(x, wasted, label="Wasted prefetches")
        ax.set_xlabel("Experiment index")
        ax.set_ylabel("Count")
        ax.set_title("Useful vs wasted prefetches")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig6_prefetch_counts.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 6: Useful vs wasted prefetches")
    except KeyError as e:
        print(f"Missing column for Figure 6: {e}")

    # ---------- Figure 7: Prefetch success ratio ----------
    try:
        psr = df["PrefetchSuccessRate"]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, psr)
        ax.set_xlabel("Experiment index")
        ax.set_ylabel("Prefetch Success Rate")
        ax.set_title("Prefetch success ratio across experiments")
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig7_prefetch_success_ratio.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 7: Prefetch success ratio")
    except KeyError:
        print("Column 'PrefetchSuccessRate' not found for Figure 7")

    # ---------- Figure 8: Admissions / evictions / prefetches ----------
    try:
        evictions = df["NumCacheEviction"]
        prefetches = df["NumPrefetches"]
        rejections = df["NumCacheRejection"]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, evictions, label="Evictions")
        ax.plot(x, prefetches, label="Prefetches")
        ax.plot(x, rejections, label="Rejections")
        ax.set_xlabel("Experiment index")
        ax.set_ylabel("Count")
        ax.set_title("Cache activity: evictions, prefetches, rejections")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / "eval_fig8_cache_activity.png", dpi=300)
        plt.close(fig)
        print("Saved Figure 8: Cache activity (admit/evict/prefetch)")
    except KeyError as e:
        print(f"Missing column for Figure 8: {e}")


if __name__ == "__main__":
    main()

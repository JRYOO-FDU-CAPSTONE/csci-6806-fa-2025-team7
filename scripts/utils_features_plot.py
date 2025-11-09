#!/usr/bin/env python3
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def generate_policy_figures(csv_path):
    plt.rcParams.update({
        "font.family": "Times New Roman",
        "font.size": 10,
        "axes.titlesize": 10,
        "axes.labelsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10
    })

    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fig_dir = os.path.join(repo_root, "runs", "example", "rejectx")
    os.makedirs(fig_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(df["Target Cache Size"], df["Service Time Saved Ratio"],
                color="orange", alpha=0.8, edgecolor="black")
    plt.title("Service Time Saved Ratio vs Target Cache Size", fontweight="bold")
    plt.xlabel("Target Cache Size (GB)", fontweight="bold")
    plt.ylabel("Service Time Saved Ratio", fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "service_time_saved_vs_cache_size.png"), dpi=300)

    plt.figure(figsize=(8, 6))
    plt.plot(df["Target Cache Size"], df["IOPSSavedRatio"],
             marker="o", color="green", alpha=0.8)
    plt.title("IOPS Saved Ratio vs Target Cache Size", fontweight="bold")
    plt.xlabel("Target Cache Size (GB)", fontweight="bold")
    plt.ylabel("IOPS Saved Ratio", fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "iops_saved_vs_cache_size.png"), dpi=300)

    plt.figure(figsize=(8, 6))
    plt.bar(df["Target Cache Size"], df["Mean Time In System (s)"],
            color="purple", alpha=0.8)
    plt.title("Mean Time In System vs Target Cache Size", fontweight="bold")
    plt.xlabel("Target Cache Size (GB)", fontweight="bold")
    plt.ylabel("Mean Time In System (s)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "mean_time_vs_cache_size.png"), dpi=300)

    plt.figure(figsize=(8, 6))
    plt.bar(df["Target Cache Size"], df["Write Rate (MB/s)"],
            color="skyblue", alpha=0.8)
    plt.title("Write Rate vs Target Cache Size", fontweight="bold")
    plt.xlabel("Target Cache Size (GB)", fontweight="bold")
    plt.ylabel("Write Rate (MB/s)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "write_rate_vs_cache_size.png"), dpi=300)

    print(f"\n✅ Figures saved in: {fig_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    args = parser.parse_args()
    generate_policy_figures(args.input)

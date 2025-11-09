import os
import pandas as pd
import matplotlib.pyplot as plt

csv_file = "runs/example/rejectx/Region1/legacy_access_summary.csv"
figures_dir = "runs/example/rejectx/Region1/figures"
os.makedirs(figures_dir, exist_ok=True)

df = pd.read_csv(csv_file)
print("✅ Columns in CSV:", df.columns.tolist())

plt.rcParams.update({
    "font.size": 13,
    "axes.labelweight": "bold",
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
})

# === 1️⃣ Top 10 Keys by Access Count ===
top_keys = df.sort_values("access_count", ascending=False).head(10)
plt.figure(figsize=(8, 6))
plt.bar(top_keys["key"].astype(str), top_keys["access_count"], color="skyblue")
plt.xlabel("Key", fontsize=12, fontweight="bold")
plt.ylabel("Access Count", fontsize=12, fontweight="bold")
plt.title("Top 10 Keys by Access Count", fontsize=15, fontweight="bold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "utils_top10_access_count.png"))
plt.close()

# === 2️⃣ Access Count vs Average Block Size ===
plt.figure(figsize=(8, 6))
plt.scatter(df["access_count"], df["avg_block_size"], alpha=0.6, color="orange", edgecolor="black")
plt.xlabel("Access Count", fontsize=12, fontweight="bold")
plt.ylabel("Average Block Size (bytes)", fontsize=12, fontweight="bold")
plt.title("Access Count vs Average Block Size", fontsize=15, fontweight="bold")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "utils_access_count_vs_block_size.png"))
plt.close()

# === 3️⃣ Histogram of Average Block Sizes ===
plt.figure(figsize=(8, 6))
plt.hist(df["avg_block_size"], bins=40, color="purple", alpha=0.7)
plt.xlabel("Average Block Size (bytes)", fontsize=12, fontweight="bold")
plt.ylabel("Frequency", fontsize=12, fontweight="bold")
plt.title("Distribution of Average Block Sizes", fontsize=15, fontweight="bold")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "utils_block_size_distribution.png"))
plt.close()

# === 4️⃣ Accesses Over Time (if timestamps are usable) ===
if "avg_timestamp" in df.columns:
    plt.figure(figsize=(8, 6))
    plt.plot(df["avg_timestamp"], df["access_count"], color="green", alpha=0.6)
    plt.xlabel("Average Timestamp", fontsize=12, fontweight="bold")
    plt.ylabel("Access Count", fontsize=12, fontweight="bold")
    plt.title("Access Frequency Over Time", fontsize=15, fontweight="bold")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "utils_access_over_time.png"))
    plt.close()

print(f"✅ All figures saved to: {figures_dir}")

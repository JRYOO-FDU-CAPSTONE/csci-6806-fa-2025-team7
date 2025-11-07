import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# CSV file  Region2
csv_path = os.path.join(
    base_dir,
    "../runs/small_test_evict_region2/small_test_evict_region2/201910_Region2_0_0.1/offline_analysis_ea_5892.86.csv"
)

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

# Output directory = same folder as CSV
output_dir = os.path.dirname(csv_path)
print(f"Saving figures in: {output_dir}")

df = pd.read_csv(csv_path)
print(f"Loaded data from: {csv_path}")
print(f"Columns: {list(df.columns)}")
print(f"Total records shown: {len(df)}")

plt.figure(figsize=(8, 6))
plt.scatter(df["Cache Size (GB)"], df["Service Time Saved Ratio"], color="steelblue", alpha=0.7)
plt.title("Region 2 Eviction Policy: Cache Size vs Service Time Saved Ratio")
plt.xlabel("Cache Size (GB)")
plt.ylabel("Service Time Saved Ratio")
plt.grid(True, linestyle="--", alpha=0.5)

fig1_path = os.path.join(output_dir, "eviction_cache_vs_service.png")
plt.savefig(fig1_path, dpi=300, bbox_inches="tight")
print(f" Saved plot: {fig1_path}")
plt.close()

plt.figure(figsize=(8, 6))
plt.scatter(df["Write Rate (MB/s)"], df["IOPSSavedRatio"], color="darkorange", alpha=0.7)
plt.title("Region 2 Eviction Policy: Write Rate vs IOPS Saved Ratio")
plt.xlabel("Write Rate (MB/s)")
plt.ylabel("IOPS Saved Ratio")
plt.grid(True, linestyle="--", alpha=0.5)

fig2_path = os.path.join(output_dir, "eviction_write_vs_iops.png")
plt.savefig(fig2_path, dpi=300, bbox_inches="tight")
print(f" Saved plot: {fig2_path}")
plt.close()

print("\n Eviction analysis completed successfully! Figures are saved in the runs folder.")

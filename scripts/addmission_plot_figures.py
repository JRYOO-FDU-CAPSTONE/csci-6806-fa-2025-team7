import pandas as pd
import matplotlib.pyplot as plt
import os

csv_file = "../runs/small_test/small_test/201910_Region1_0_0.1/offline_analysis_ea_5892.86.csv"
figures_dir = "../runs/small_test/figures"

os.makedirs(figures_dir, exist_ok=True)

df = pd.read_csv(csv_file)

print("Columns in CSV:", df.columns)

# 1. Write Rate vs Cache Size
plt.figure(figsize=(8,6))
plt.scatter(df['Write Rate (MB/s)'], df['Cache Size (GB)'], c='blue', label='Write Rate vs Cache Size')
plt.xlabel('Write Rate (MB/s)')
plt.ylabel('Cache Size (GB)')
plt.title('Write Rate vs Cache Size')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "admission_write_rate_vs_cache_size.png"))
plt.close()

# 2. Service Time Saved Ratio vs Write Rate
plt.figure(figsize=(8,6))
plt.plot(df['Write Rate (MB/s)'], df['Service Time Saved Ratio'], marker='o', linestyle='-', color='green', label='Service Time Saved Ratio')
plt.xlabel('Write Rate (MB/s)')
plt.ylabel('Service Time Saved Ratio')
plt.title('Service Time Saved Ratio vs Write Rate')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "admission_service_time_saved_ratio.png"))
plt.close()

# 3. IOPS Saved Ratio vs Write Rate
plt.figure(figsize=(8,6))
plt.plot(df['Write Rate (MB/s)'], df['IOPSSavedRatio'], marker='x', linestyle='--', color='red', label='IOPS Saved Ratio')
plt.xlabel('Write Rate (MB/s)')
plt.ylabel('IOPS Saved Ratio')
plt.title('IOPS Saved Ratio vs Write Rate')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "admission_iops_saved_ratio.png"))
plt.close()

print("Figures saved in:", figures_dir)

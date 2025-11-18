import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("runs/A5/ablation_summary.csv")

sizes = [128, 256]
sub = df[df["CacheSize(GB)"].isin(sizes)].sort_values("CacheSize(GB)")
labels = sub["CacheSize(GB)"].astype(str) + " GB"

plt.figure()
plt.bar(labels, sub["HitRate"])
plt.xlabel("Cache size")
plt.ylabel("Hit rate")
plt.title("Effect of cache size on hit rate (LRU)")
plt.savefig("figures/ablation_fig9_cache_size_hit_rate.png", bbox_inches="tight")

plt.figure()
plt.bar(labels, sub["AvgEvictAge(s)"])
plt.xlabel("Cache size")
plt.ylabel("Average eviction age (s)")
plt.title("Effect of cache size on eviction age (LRU)")
plt.savefig("figures/ablation_fig10_cache_size_eviction_age.png", bbox_inches="tight")

plt.figure()
plt.bar(labels, sub["IOPS_Saved_Ratio"])
plt.xlabel("Cache size")
plt.ylabel("IOPS saved ratio")
plt.title("Effect of cache size on IOPS saved (LRU)")
plt.savefig("figures/ablation_fig11_cache_size_iops_saved.png", bbox_inches="tight")

plt.figure()
plt.bar(labels, sub["ClientMBps"])
plt.xlabel("Cache size")
plt.ylabel("Client bandwidth (MB/s)")
plt.title("Effect of cache size on client bandwidth (LRU)")
plt.savefig("figures/ablation_fig12_cache_size_client_bw.png", bbox_inches="tight")

plt.figure()
plt.bar(labels, sub["FlashWriteMBps"])
plt.xlabel("Cache size")
plt.ylabel("Flash write rate (MB/s)")
plt.title("Effect of cache size on flash write rate (LRU)")
plt.savefig("figures/ablation_fig13_cache_size_flash_write.png", bbox_inches="tight")

plt.figure()
plt.bar(labels, sub["TotalChunkHits"])
plt.xlabel("Cache size")
plt.ylabel("Total chunk hits")
plt.title("Effect of cache size on chunk hits (LRU)")
plt.savefig("figures/ablation_fig14_cache_size_chunk_hits.png", bbox_inches="tight")

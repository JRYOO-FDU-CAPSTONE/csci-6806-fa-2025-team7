import argparse
from pathlib import Path
import matplotlib.pyplot as plt


def generate_synthetic_episodes(num_points: int = 2000, boundaries=None):
    """
    Generate a simple synthetic episode/region series.

    boundaries: list of request indices where each new episode starts.
    Example: [0, 500, 1100, 1600, 2000] -> 4 episodes (E0..E3).
    """
    if boundaries is None:
        boundaries = [0, 500, 1100, 1600, 2000]

    xs = []
    eps = []
    cur = 0
    for i in range(len(boundaries) - 1):
        start, end = boundaries[i], boundaries[i + 1]
        for _ in range(start, end):
            xs.append(cur)
            eps.append(i)
            cur += 1

    return xs, eps


def main():
    parser = argparse.ArgumentParser(
        description="Generate episode segmentation background figure."
    )
    parser.add_argument(
        "--out",
        default="figures/background_episodes_example.png",
        help="Output image path",
    )

    args = parser.parse_args()

    Path("figures").mkdir(parents=True, exist_ok=True)

    xs, eps = generate_synthetic_episodes()

    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.step(xs, eps, where="post")
    ax.set_xlabel("Request index")
    ax.set_ylabel("Episode ID")
    ax.set_title("Illustrative episode segmentation of a workload trace")

    unique_eps = sorted(set(eps))
    ax.set_yticks(unique_eps)
    ax.set_yticklabels([f"E{i}" for i in unique_eps])

    fig.tight_layout()
    out_path = Path(args.out)
    fig.savefig(out_path, dpi=300)
    print(f"Saved episode background figure to {out_path}")


if __name__ == "__main__":
    main()

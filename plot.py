import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_chipping_times(results):
    """Plot COG vs NITF chipping times."""
    filenames = list(results.keys())
    cog_times = [results[filename]["cog_time"] for filename in filenames]
    nitf_times = [results[filename]["nitf_time"] for filename in filenames]

    # Plot comparison of COG and NITF chipping times
    x = np.arange(len(filenames))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width / 2, cog_times, width, label="COG Chipping Time (s)")
    rects2 = ax.bar(x + width / 2, nitf_times, width, label="NITF Chipping Time (s)")

    # Add labels, title, and custom x-axis tick labels
    ax.set_xlabel("Files")
    ax.set_ylabel("Chipping Time (seconds)")
    ax.set_title("COG vs NITF Chipping Times")
    ax.set_xticks(x)
    ax.set_xticklabels(filenames, rotation=90)
    ax.legend()

    fig.tight_layout()
    plt.savefig("chipping_times_comparison.png")
    plt.show()


def plot_filesize_vs_chipping_time(results):
    """Plot NITF file size vs chipping times."""
    filenames = list(results.keys())
    nitf_filesizes = [
        results[filename]["nitf_filesize"] / (1024 * 1024) for filename in filenames
    ]  # convert to MB
    nitf_times = [results[filename]["nitf_time"] for filename in filenames]

    # Scatter plot for NITF file size vs NITF chipping time
    plt.figure(figsize=(10, 6))
    plt.scatter(nitf_filesizes, nitf_times, color="blue", label="NITF Chipping Time")

    # Add trend line
    z = np.polyfit(nitf_filesizes, nitf_times, 1)
    p = np.poly1d(z)
    plt.plot(nitf_filesizes, p(nitf_filesizes), "r--", label="Trendline")

    plt.xlabel("NITF File Size (MB)")
    plt.ylabel("NITF Chipping Time (seconds)")
    plt.title("NITF File Size vs Chipping Time")
    plt.legend()

    plt.savefig("nitf_filesize_vs_chipping_time.png")
    plt.show()


def load_results():
    """Load results from results.json."""
    results_dest = Path(__file__).parent / "results.json"
    with results_dest.open() as f:
        results = json.load(f)
    return results


def main():
    results = load_results()

    # Generate plots
    plot_chipping_times(results)
    plot_filesize_vs_chipping_time(results)


if __name__ == "__main__":
    main()

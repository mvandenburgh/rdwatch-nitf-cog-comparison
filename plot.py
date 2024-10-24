import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_chipping_times(results, name: str):
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
    plt.savefig(f"chipping_times_comparison_{name}.png")
    plt.show()


def plot_filesize_vs_chipping_time(results, name: str):
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

    plt.savefig(f"nitf_filesize_vs_chipping_time_{name}.png")
    plt.show()


def load_results():
    """Load results from results.json."""
    results = []
    for file in ['results.json', 'results_with_vsil_curl_chunk_size.json']:
        results_dest = Path(__file__).parent / file
        with results_dest.open() as f:
            results.append(json.load(f))
    return results


def main():
    results = load_results()

    # Generate plots
    plot_chipping_times(results[0], 'without_vsil_curl_chunk_size')
    plot_filesize_vs_chipping_time(results[0], 'without_vsil_curl_chunk_size')
    plot_chipping_times(results[1], 'with_vsil_curl_chunk_size')
    plot_filesize_vs_chipping_time(results[1], 'with_vsil_curl_chunk_size')


if __name__ == "__main__":
    main()

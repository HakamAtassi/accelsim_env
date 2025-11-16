
import json
import matplotlib.pyplot as plt, os

def plot_kernel(ax, kernel_page_access):
    base_addr = 0x7f8ea6e000
    stride = 256  # distance between pages

    addresses = [base_addr + i * stride for i, _ in enumerate(kernel_page_access)]
    counts = [v[1] for v in kernel_page_access]

    # Make bars touch (width = stride)
    ax.bar(addresses, counts, width=stride, align='edge')
    ax.set_xlabel("Address (hex)")
    ax.set_ylabel("Accesses")


if __name__ == "__main__":
    for dirpath, dirnames, filenames in os.walk("../rodinia/"):
        for d in dirnames:
            path = os.path.join(dirpath, d)
            json_path = os.path.join(path, "memory_stats_json.txt")
            if not os.path.isfile(json_path):
                continue

            print(f"Processing {json_path}")
            with open(json_path) as f:
                mem_hotness = json.load(f)

            fig, axs = plt.subplots(len(mem_hotness), 1, figsize=(8, 3 * len(mem_hotness)))
            if len(mem_hotness) == 1:
                axs = [axs]

            for ax, kernel in zip(axs, mem_hotness):
                plot_kernel(ax, kernel)

            plt.tight_layout()
            out_path = os.path.join(path, f"{d}.png")
            plt.savefig(out_path, dpi=150)
            plt.close(fig)
            print(f"Saved {out_path}")

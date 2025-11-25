import matplotlib.pyplot as plt
import numpy as np
import math
import re
import os

#########################
## TRACE FILE GRAMMARS ##
#########################

DRAM_files = []
HETERO_files = []
HBM_files = []

DRAM_data = {}  # data as json (per-workload)
HETERO_data = {}
HBM_data = {}

workloads = []

# Very fast regex to match either "gpu_sim_cycle" or "gpu_sim_cycles" followed by = and a number
_cycle_re = re.compile(r"\b(gpu_sim_cycles?|gpu_sim_cycle)\s*=\s*(\d+)\b")

def jsonify_outputs(contents):
    """
    Parse the entire file contents with a compiled regex.
    Returns dict: { 'gpu_sim_cycle' : [ints,...], ... }
    This is much faster than pyparsing for this simple task.
    """
    results_json = {}
    for m in _cycle_re.finditer(contents):
        name = m.group(1)
        num = int(m.group(2))
        results_json.setdefault(name, []).append(num)
    return results_json


#################
## PARSE FILES ##
#################

rodinia = "./rodinia"

# collect workload directories (ignore hidden files)
with os.scandir(rodinia) as it:
    for entry in it:
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        workloads.append(entry.name)

# build expected file paths and parse if present
for wl in workloads:
    print("Parsing workload:", wl)
    full = os.path.join(rodinia, wl)
    dram_path = os.path.join(full, f"{wl}.out_DRAM")
    hetero_path = os.path.join(full, f"{wl}.out_HETERO")
    HBM_path = os.path.join(full, f"{wl}.out_HBM")

    if os.path.exists(dram_path):
        DRAM_files.append(dram_path)
        with open(dram_path, "r") as f:
            DRAM_data[wl] = jsonify_outputs(f.read())
        # Or for streaming: DRAM_data[wl] = jsonify_outputs_stream(dram_path)
    else:
        DRAM_data[wl] = {}  # keep key for consistency

    if os.path.exists(hetero_path):
        HETERO_files.append(hetero_path)
        with open(hetero_path, "r") as f:
            HETERO_data[wl] = jsonify_outputs(f.read())
    else:
        HETERO_data[wl] = {}

    # Correctly check HBM_path (previous bug: checked hetero_path twice)
    if os.path.exists(HBM_path):
        HBM_files.append(HBM_path)
        with open(HBM_path, "r") as f:
            HBM_data[wl] = jsonify_outputs(f.read())
    else:
        HBM_data[wl] = {}

# debug prints (optional)
#print("Workloads:", workloads)
#print("DRAM files:", DRAM_files)
#print("HETERO files:", HETERO_files)
#print("HBM files:", HBM_files)


##################
# GENERATE PLOTS #
##################

def plot_speedup(workloads, DRAM_data, HETERO_data, HBM_data, outname="gpu_sim_cycle_speedup.png"):
    """
    Plot GPU cycle speedup per workload.
    - Baseline bar = 1.0 (DRAM / DRAM)
    - Speedup bars = sum(DRAM cycles) / sum(HETERO cycles) and sum(DRAM cycles) / sum(HBM cycles)
    Saves outname and returns (fig, ax).
    """
    import numpy as np
    import matplotlib.pyplot as plt

    labels = []
    baseline = []
    speedups_hetero = []
    speedups_HBM = []
    skipped = []

    # small helper to extract the gpu_sim_cycle list and sum it
    def sum_first_numeric(stats):
        # prefer canonical names first
        for key_name in ("gpu_sim_cycles", "gpu_sim_cycle"):
            if key_name in stats:
                vals = stats[key_name]
                if isinstance(vals, (list, tuple)):
                    return sum(vals)
        # fallback: find any numeric list
        for v in stats.values():
            if isinstance(v, (list, tuple)) and v and all(isinstance(x, (int, float)) for x in v):
                return sum(v)
        return 0

    for wl in workloads:
        dram_stats = DRAM_data.get(wl, {})
        hetero_stats = HETERO_data.get(wl, {})
        HBM_stats = HBM_data.get(wl, {})

        #print(f"DRAM wl: {wl}, {sum(dram_stats["gpu_sim_cycle"])}")
        #print(f"HBM wl: {wl}, {sum(HBM_stats["gpu_sim_cycle"])}")
        #print(f"HETERO wl: {wl}, {sum(hetero_stats["gpu_sim_cycle"])}")
        #print("")

        dram_sum = sum_first_numeric(dram_stats)
        hetero_sum = sum_first_numeric(hetero_stats)
        HBM_sum = sum_first_numeric(HBM_stats)

        # skip workloads with no meaningful data at all
        if dram_sum == 0 and hetero_sum == 0 and HBM_sum == 0:
            skipped.append(wl)
            continue

        labels.append(wl)
        baseline.append(1.0)

        # compute hetero speedup (DRAM / HETERO)
        speedups_hetero.append(float(dram_sum) / float(hetero_sum) if hetero_sum > 0 else np.nan)

        # compute HBM speedup (DRAM / HBM)
        speedups_HBM.append(float(dram_sum) / float(HBM_sum) if HBM_sum > 0 else np.nan)

    if not labels:
        raise ValueError("No workloads with data found to plot.")

    x = np.arange(len(labels))
    w = 0.25  # width for each of the three bars

    # Better colors
    color_dram  = "#7f7f7f"   # grey
    color_speed = "#1f7a1f"   # dark green
    color_HBM = "#4c4cff"     # soft medium blue

    fig, ax = plt.subplots(figsize=(max(6, len(labels)*0.6), 4.5))

    # three side-by-side bars: baseline (left), hetero (center), HBM (right)
    b1 = ax.bar(x - w, baseline, w, label="DRAM baseline (16ch + 0)", color=color_dram)
    b2 = ax.bar(x, speedups_hetero, w, label="Heterogenous (16ch + 16ch)", color=color_speed)
    b3 = ax.bar(x + w, speedups_HBM, w, label="HBM (0 + 16ch)", color=color_HBM)

    ax.set_title("gpu_sim_cycle speedup per workload", fontsize=12, weight="bold")
    ax.set_ylabel("Speedup")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")

    ax.axhline(1.0, linestyle="--", linewidth=0.8, alpha=0.8, color="black")

    # adaptive zoomed-in axis around 1.0, but with a minimum window
    all_vals = np.array([v for v in (speedups_hetero + speedups_HBM + [1.0])], dtype=float)
    # ignore nan when computing min/max
    finite = all_vals[np.isfinite(all_vals)]
    if finite.size:
        min_val = finite.min()
        max_val = finite.max()
        pad = max(0.02, (max_val - min_val) * 0.1)
        ymin = min(0.96, min_val - pad)
        ymax = max(1.04, max_val + pad)
        # ensure a small reasonable range
        if ymax - ymin < 0.08:
            center = (ymax + ymin) / 2.0
            ymin = max(0.0, center - 0.04)
            ymax = center + 0.04
        ax.set_ylim(ymin, ymax)
    else:
        ax.set_ylim(0.96, 1.04)

    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.legend()

    plt.tight_layout()
    plt.savefig(outname, dpi=300)
    print("Saved figure as:", outname)
    plt.show()

    if skipped:
        print("Skipped (no data):", skipped)

    return fig, ax

# call the plotting function
plot_speedup(workloads, DRAM_data, HETERO_data, HBM_data)

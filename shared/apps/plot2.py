import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import json

results = {}


configs = ["gpgpusim_HBM", "gpgpusim_DRAM", "gpgpusim_HETERO"]


results_dir = "results/"


# for every key in the dict, perform a find all for the file
# create a dict of 


def build_sums(json_list, key_path, do_avg=True):
    """
    Simple: sum or average values at a nested path.

    json_list : list of dict-like entries
    key_path  : list of keys, e.g. ["memlatstat_print", "total_dram_bytes_accessed"]
                or ["gpu_sim_cycles"]
    do_avg    : True -> return average, False -> return sum

    Missing / non-numeric entries are skipped.
    """
    total = 0.0
    count = 0

    for entry in json_list:
        cur = entry
        try:
            for k in key_path:
                cur = cur[k]
            val = float(cur)          # will raise if not numeric
        except Exception:
            # skip entries where the path is missing or value isn't numeric
            continue

        total += val
        count += 1

    if do_avg:
        return (total / count) if count else 0.0
    return total


def count_HBM_DRAM_accesses(json_list):
    HBM=0
    DRAM=0
    for kernel in json_list:
        try:
            for i, bank_accesses in enumerate(kernel["memlatstat_print"]["total_bytes_accessed"]):
                if(i<16):
                    DRAM+=sum(bank_accesses)
                else:
                    HBM+=sum(bank_accesses)
        except Exception:
            continue
    return DRAM, HBM, DRAM+HBM

def parse_data(results_dir):
    wls = os.listdir(results_dir)

    HBM_speedups = []
    DRAM_speedups = []
    HETERO_speedups = []

    HBM_occupancy = []
    DRAM_occupancy = []
    HETERO_occupancy = []

    HBM_mem_throughput = []
    DRAM_mem_throughput = []
    HETERO_mem_throughput = []

    HBM_access_percentages = []
    DRAM_access_percentages = []
    HETERO_access_percentages = []

    for wl_path in wls:
        wl_path = os.path.join("results/", wl_path)

        print(wl_path)

        HBM_path = os.path.join(wl_path, "gpgpusim_HBM/stats.json")
        DRAM_path = os.path.join(wl_path, "gpgpusim_DRAM/stats.json")
        HETERO_path = os.path.join(wl_path, "gpgpusim_HETERO/stats.json")

        HBM_json = json.loads(open(HBM_path).read())
        DRAM_json = json.loads(open(DRAM_path).read())
        HETERO_json = json.loads(open(HETERO_path).read())


        # first create sums across all kernels

        HBM_avg_gpu_sim_cycles = build_sums(HBM_json, ["gpu_sim_cycles"], False)
        DRAM_avg_gpu_sim_cycles = build_sums(DRAM_json, ["gpu_sim_cycles"], False)
        HETERO_avg_gpu_sim_cycles = build_sums(HETERO_json, ["gpu_sim_cycles"], False)

        HBM_avg_gpu_occupancy = build_sums(HBM_json, ["gpu_occupancy"], True)
        DRAM_avg_gpu_occupancy = build_sums(DRAM_json, ["gpu_occupancy"], True)
        HETERO_avg_gpu_occupancy = build_sums(HETERO_json, ["gpu_occupancy"], True)

        HBM_total_dram_bytes_accessed = build_sums(HBM_json, ["memlatstat_print", "total_dram_bytes_accessed"], False)
        DRAM_total_dram_bytes_accessed = build_sums(DRAM_json, ["memlatstat_print", "total_dram_bytes_accessed"], False)
        HETERO_total_dram_bytes_accessed = build_sums(HETERO_json, ["memlatstat_print", "total_dram_bytes_accessed"], False)

        print(DRAM_total_dram_bytes_accessed)
        print(DRAM_avg_gpu_sim_cycles)
        print(f"mem throughput = {DRAM_total_dram_bytes_accessed/DRAM_avg_gpu_sim_cycles}")



        ### CREATE PLOTS ###


        # your scalar cycle values

        DRAM_speedups.append(DRAM_avg_gpu_sim_cycles/DRAM_avg_gpu_sim_cycles)
        HBM_speedups.append(DRAM_avg_gpu_sim_cycles/HBM_avg_gpu_sim_cycles)
        HETERO_speedups.append(DRAM_avg_gpu_sim_cycles/HETERO_avg_gpu_sim_cycles)



        DRAM_occupancy.append(DRAM_avg_gpu_occupancy)
        HBM_occupancy.append(HBM_avg_gpu_occupancy)
        HETERO_occupancy.append(HETERO_avg_gpu_occupancy)


        DRAM_mem_throughput.append(DRAM_total_dram_bytes_accessed/DRAM_avg_gpu_sim_cycles)
        HBM_mem_throughput.append(HBM_total_dram_bytes_accessed/HBM_avg_gpu_sim_cycles)
        HETERO_mem_throughput.append(HETERO_total_dram_bytes_accessed/HETERO_avg_gpu_sim_cycles)


        DRAM_accesses, HBM_accesses, total = count_HBM_DRAM_accesses(HETERO_json)
        HETERO_access_percentages.append(((DRAM_accesses/total, HBM_accesses/total)))

        HBM_accesses, DRAM_accesses, total = count_HBM_DRAM_accesses(HBM_json)
        HBM_access_percentages.append((DRAM_accesses/total, HBM_accesses/total))

        DRAM_accesses, HBM_accesses, total = count_HBM_DRAM_accesses(DRAM_json)
        DRAM_access_percentages.append((DRAM_accesses/total, HBM_accesses/total))



    color_dram  = "#7f7f7f"   # grey
    color_hetero = "#1f7a1f"   # dark green
    color_HBM = "#4c4cff"     # soft medium blue

    ## PLOT SPEED UP ON FIRST ROW ##

    n = len(wls)
    x = np.arange(n)               # one x position per workload

    # convert lists to numpy arrays (safer)
    d_sp  = np.array(DRAM_speedups)
    h_sp  = np.array(HBM_speedups)
    he_sp = np.array(HETERO_speedups)

    d_occ  = np.array(DRAM_occupancy)
    h_occ  = np.array(HBM_occupancy)
    he_occ = np.array(HETERO_occupancy)

    # grouping parameters
    total_width = 0.8               # fraction of space taken by all bars at a single x
    n_configs = 3
    bar_width = total_width / n_configs
    offsets = (np.arange(n_configs) - (n_configs - 1) / 2) * bar_width

    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)

    # --- Top: speedups (grouped per workload) ---

    axes[0].axhline(1.0, linestyle="--", linewidth=0.8, alpha=0.8, color="black")
    axes[0].bar(x + offsets[0], d_sp, width=bar_width, label='DRAM', color =color_dram)
    axes[0].bar(x + offsets[1], h_sp, width=bar_width, label='HBM', color =color_hetero)
    axes[0].bar(x + offsets[2], he_sp, width=bar_width, label='HETERO', color =color_HBM)
    axes[0].set_ylabel('Speedup (vs DRAM)')
    axes[0].legend()
    axes[0].set_title('Speedups per workload')


    ax2 = axes[0].twinx()
    ax2.plot(x, DRAM_mem_throughput, marker="o", linestyle="-", linewidth=2, label="Throughput", color="red")
    ax2.set_ylabel("Throughput (bytes/cycle)")
    #ax2.ticklabel_format(style='sci', axis='y', scilimits=(9,9))

    # --- middle: occupancy (grouped per workload) ---
    axes[1].bar(x + offsets[0], d_occ, width=bar_width, label='DRAM', color =color_dram)
    axes[1].bar(x + offsets[1], h_occ, width=bar_width, label='HBM', color =color_hetero)
    axes[1].bar(x + offsets[2], he_occ, width=bar_width, label='HETERO', color=color_HBM)
    axes[1].set_ylabel('Occupancy')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(wls, rotation=45, ha='right')
    axes[1].legend()
    axes[1].set_title('Occupancy per workload')

    # --- Bottom: occupancy (grouped per workload) ---
    # here, plot for every workload and memory type a bar, that sums to 1, with 2 colors that represent HBM and DRAM accesses as a percentage. 
    #HBM_access_percentages = [] lists of tuples...
    #DRAM_access_percentages = []
    #HETERO_access_percentages = []



    # unpack tuples
    dram_dram, dram_hbm = zip(*DRAM_access_percentages)
    hbm_dram,  hbm_hbm  = zip(*HBM_access_percentages)
    het_dram,  het_hbm  = zip(*HETERO_access_percentages)

    # convert to numpy arrays (optional)
    dram_dram = np.array(dram_dram)
    dram_hbm  = np.array(dram_hbm)
    hbm_dram  = np.array(hbm_dram)
    hbm_hbm   = np.array(hbm_hbm)
    het_dram  = np.array(het_dram)
    het_hbm   = np.array(het_hbm)

    # DRAM config bars
    axes[2].bar(x + offsets[0], dram_dram, width=bar_width, color=color_dram, hatch="//", lw=0.6, edgecolor="black", label="DRAM bytes")
    axes[2].bar(x + offsets[0], dram_hbm,  width=bar_width, bottom=dram_dram, color=color_dram, edgecolor="black", lw=0.6,label="HBM bytes")

    # HBM config bars
    axes[2].bar(x + offsets[1], hbm_dram, width=bar_width, color=color_hetero, hatch="//", edgecolor="black", lw=0.6)
    axes[2].bar(x + offsets[1], hbm_hbm, width=bar_width, bottom=hbm_dram, color=color_hetero, edgecolor="black", lw=0.6)

    # HETERO config bars
    axes[2].bar(x + offsets[2], het_dram, width=bar_width, color=color_HBM, hatch="//", edgecolor="black", lw=0.6)
    axes[2].bar(x + offsets[2], het_hbm, width=bar_width, bottom=het_dram, color=color_HBM, edgecolor="black", lw=0.6)

    axes[2].set_ylabel("Fraction of bytes")
    #axes[2].set_ylim(0, 1)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(wls, rotation=45, ha="right")
    axes[2].set_title("HBM / DRAM Access Fraction per Workload")

    # Legend (only uses the first two bars created)
    axes[2].legend(loc="upper right")




    axes[0].set_ylim(0.96, 1.04)

    plt.tight_layout()
    plt.savefig("out.png", dpi=150)




    exit(1)











if __name__ == "__main__":
    parse_data(results_dir)

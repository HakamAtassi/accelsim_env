import os
import glob
import subprocess
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed

workload_dir = "/accel-sim/gpu-app-collection/bin/12.8/release/"
command = lambda KLIST, GPGPU_CFG, TRACE_CFG: f"$ACCELSIM_OUT -trace {KLIST} -config {GPGPU_CFG} -config {TRACE_CFG}"

class SimulationJob:
    def __init__(self, workload_name, KLIST, gpgpu_cfg="SM86_RTX3070/gpgpusim_DRAM.config", trace_cfg="SM86_RTX3070/trace.config"):

        self.gpgpu_cfg = f"$ACCELSIM_FRAMEWORK/gpu-simulator/gpgpu-sim/configs/tested-cfgs/{gpgpu_cfg}"
        self.trace_cfg = f"$ACCELSIM_FRAMEWORK/gpu-simulator/configs/tested-cfgs/{trace_cfg}"

        self.workload_name = workload_name
        self.cfg_name = self.gpgpu_cfg.split(".")[-2].split("/")[-1]

        self.cwd = os.path.join("results", self.workload_name, self.cfg_name)

        self.output_file = os.path.join(self.cwd)

        self.KLIST = KLIST

        self.command = command(self.KLIST, self.gpgpu_cfg, self.trace_cfg)

    def run(self):
        print(f"Running {self.command}")

        # Create a directory for this workload
        os.makedirs(self.cwd, exist_ok=True)

        # Run the command inside that directory and capture output
        result = subprocess.run(
            self.command,
            shell=True,
            cwd=self.cwd,
            capture_output=True,   # capture stdout + stderr
            text=True              # return strings instead of bytes
        )

        output_text = result.stdout + "\n" + result.stderr


        with open(self.cwd + "/out.txt", "w+") as f:
            f.write(output_text)

        #print(f"Wrote output to {self.cwd + "/out.txt"}")


def run_simulation_job(sim: SimulationJob):
    sim.run()
    return sim.workload_name

def sweep_jobs(gpgpu_config):
    """Run all jobs for a given config"""
    env = os.environ.copy()

    jobs = []
    for wl in rodinia_workloads:
        pattern = os.path.join(path, "**", wl, "**", "kernelslist.g")
        matches = glob.glob(pattern, recursive=True)

        if not matches:
            print(f"No kernelslist.g found for {wl}")
            continue

        KLIST = matches[0]

        sim = SimulationJob(
            wl,
            KLIST,
            gpgpu_cfg=gpgpu_config,
            trace_cfg="SM86_RTX3070/trace.config"
        )
        jobs.append(sim)


    # ---- RUN WITH AT MOST 5 IN PARALLEL ----
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_simulation_job, job): job for job in jobs}

        for future in as_completed(futures):
            job = futures[future]
            try:
                result = future.result()
                print(f"[DONE] {result}")
            except Exception as e:
                print(f"[ERROR] {job.workload_name}: {e}")





rodinia_workloads=[
    "bfs-rodinia-2.0-ft",
    "nn-rodinia-2.0-ft",
    "hotspot-rodinia-2.0-ft",
    "heartwall-rodinia-2.0-ft",
    "lud-rodinia-2.0-ft",
    "nw-rodinia-2.0-ft",
    "pathfinder-rodinia-2.0-ft",
    "srad_v2-rodinia-2.0-ft",

#"cutlass_00_basic_gemm",
#"cutlass_05_batched_gemm",
#"cutlass_35_gemm_softmax",
#"cutlass_05_batched_gemm",
#"cutlass_41_fused_multi_head_attention_backward",
#"cutlass_41_fused_multi_head_attention_fixed_seqlen",
#"cutlass_41_fused_multi_head_attention_variable_seqlen",
#"pagerank",
#"pagerank_spmv",
#"mem_bw",
#"lonestar-*",
#"polybench-*"
]

gpgpu_configs = [
    "SM86_RTX3070/gpgpusim_DRAM.config",
    "SM86_RTX3070/gpgpusim_HBM.config",
    "SM86_RTX3070/gpgpusim_HETERO.config"
]

framework = os.environ["ACCELSIM_FRAMEWORK"]
path = os.path.join(framework, "hw_run/traces/device-0/12.8")



if __name__ == "__main__":

    for config in gpgpu_configs:
        print(f"=== RUNNING FOR CONFIG {config.upper()} ===")
        sweep_jobs(config)

import argparse
import os


YOUR_ACCELSIM_FORK = None # Put your links here (as ssh)
YOUR_GPGPU_FORK = None # ditto

ACCELSIM_UPSTREAM = "https://github.com/accel-sim/accel-sim-framework.git"
GPGPU_UPSTREAM = "https://github.com/accel-sim/gpgpu-sim_distribution.git"


parser = argparse.ArgumentParser(
                    prog='host_init',
                    description='Sets up the neccesary repos for Accelsim and GPGPU-sim')

parser.add_argument('--use-fork', type=bool)

args = parser.parse_args()

if __name__ == "__main__":
    if(args.use_fork):
        print("Using FORKS")
        if(YOUR_ACCELSIM_FORK == None or YOUR_GPGPU_FORK == None):
            print(f"ERROR: you used a fork but never set your fork links.")
            exit(1)

        ACCELSIM=YOUR_ACCELSIM_FORK
        GPGPU_UPSTREAM=YOUR_GPGPU_FORK

    os.system(f"git clone {ACCELSIM_UPSTREAM} shared/accel-sim-framework")
    os.system(f"git clone {GPGPU_UPSTREAM} shared/accel-sim-framework/gpu-simulator/gpgpu-sim")


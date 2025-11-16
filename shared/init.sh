
ACCELSIM_FRAMEWORK=/root/Repos/shared/accel-sim-framework
ACCELSIM_DATA=/accel-sim
export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$CUDA_INSTALL_PATH/bin:$PATH
export CUDA_VISIBLE_DEVICES=0


# install GPGPU #
cd $ACCELSIM_FRAMEWORK
pip3 install -r requirements.txt
source ./gpu-simulator/setup_environment.sh
make -j12 -C ./gpu-simulator/


# install nvbit
cd $ACCELSIM_FRAMEWORK
./util/tracer_nvbit/install_nvbit.sh
make -C ./util/tracer_nvbit/


# run example trace
cd $ACCELSIM_FRAMEWORK/util/tracer_nvbit
make -C nvbit_release/test-apps
LD_PRELOAD=$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/tracer_tool.so ./nvbit_release/test-apps/vectoradd/vectoradd


# make gpgpu workloads (rodinia)
cd $ACCELSIM_DATA
source ./gpu-app-collection/src/setup_environment
make -j -C ./gpu-app-collection/src rodinia_2.0-ft
make -C ./gpu-app-collection/src data



## YOU ARE NOW SET UP #
## CLOSE AND RESTART CONTAINER TO PROCEED!! ##


ACCELSIM_FRAMEWORK=/root/Repos/shared/accel-sim-framework
ACCELSIM_DATA=/accel-sim
export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$CUDA_INSTALL_PATH/bin:$PATH
export CUDA_VISIBLE_DEVICES=0


cd $ACCELSIM_FRAMEWORK
source ./gpu-simulator/setup_environment.sh # source (again)

# Run accelsim
./util/tracer_nvbit/run_hw_trace.py -B rodinia_2.0-ft -D 0 # IDFK what this does


# run as SASS (GPGPU)
./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C RTX3070-SASS -T ./hw_run/traces/device-0/12.8/ -N myTest

# monitor jobs
./util/job_launching/monitor_func_test.py -v -N myTest

# run as PTX (trace based)
./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C RTX3070-PTX -N myTest-PTX

# Monitor again
./util/job_launching/monitor_func_test.py -v -N myTest-PTX


# Run a directed test 
./gpu-simulator/bin/release/accel-sim.out -trace ./hw_run/traces/device-0/12.8/backprop-rodinia-2.0-ft/4096___data_result_4096_txt/traces/kernelslist.g -config ./gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM86_RTX3070/gpgpusim.config -config ./gpu-simulator/configs/tested-cfgs/SM86_RTX3070/trace.config 

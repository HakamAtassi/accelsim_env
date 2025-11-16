ACCELSIM_FRAMEWORK=/root/Repos/shared/accel-sim-framework
ACCELSIM_DATA=/accel-sim
export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$CUDA_INSTALL_PATH/bin:$PATH
export CUDA_VISIBLE_DEVICES=0

ACCELSIM_OUT=$ACCELSIM_FRAMEWORK/gpu-simulator/bin/release/accel-sim.out
GPGPU_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM86_RTX3070/gpgpusim.config
TRACE_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/configs/tested-cfgs/SM86_RTX3070/trace.config

APPS=$ACCELSIM_FRAMEWORK/../apps
cd $APPS

nvcc main.cu -o main
./main

# trace
LD_PRELOAD=$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/tracer_tool.so ./main


# post process
$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/traces-processing/post-traces-processing ./traces/kernelslist_ctx_0x56215337c970


# run
$ACCELSIM_OUT -trace ./traces/kernelslist.g -config $GPGPU_CFG -config $TRACE_CFG




## NN RUN


cd $ACCELSIM_FRAMEWORK
source ./gpu-simulator/setup_environment.sh
make -j12 -C ./gpu-simulator/
cd $APPS/rodinia

$ACCELSIM_OUT -trace $ACCELSIM_FRAMEWORK/hw_run/traces/device-0/12.8/bfs-rodinia-2.0-ft/__data_graph4096_txt___data_graph4096_result_txt/traces/kernelslist.g -config $GPGPU_CFG -config $TRACE_CFG > bfs.out


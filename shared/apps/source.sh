export ACCELSIM_FRAMEWORK=/root/Repos/shared/accel-sim-framework
export ACCELSIM_DATA=/accel-sim

export ACCELSIM_OUT=$ACCELSIM_FRAMEWORK/gpu-simulator/bin/release/accel-sim.out
export GPGPU_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM86_RTX3070/gpgpusim.config
export TRACE_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/configs/tested-cfgs/SM86_RTX3070/trace.config
export APPS=$ACCELSIM_FRAMEWORK/../apps

export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$CUDA_INSTALL_PATH/bin:$PATH
export CUDA_VISIBLE_DEVICES=0


source $ACCELSIM_FRAMEWORK/gpu-simulator/setup_environment.sh

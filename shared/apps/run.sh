#!/usr/bin/env bash
set -e

cd $ACCELSIM_FRAMEWORK
source ./gpu-simulator/setup_environment.sh
make -j12 -C ./gpu-simulator/

cd $APPS/rodinia

WORKLOADS=(
  bfs-rodinia-2.0-ft
  hotspot-rodinia-2.0-ft
  heartwall-rodinia-2.0-ft
  lud-rodinia-2.0-ft
  nn-rodinia-2.0-ft
  nw-rodinia-2.0-ft
  pathfinder-rodinia-2.0-ft
  srad_v2-rodinia-2.0-ft
  streamcluster-rodinia-2.0-ft
)

for wl in "${WORKLOADS[@]}"; do
  mkdir -p $wl && cd $wl
  KLIST=$(find "$ACCELSIM_FRAMEWORK/hw_run/traces/device-0" -type f -path "*$wl*/kernelslist.g" -print -quit)
  $ACCELSIM_OUT -trace $KLIST -config $GPGPU_CFG -config $TRACE_CFG > ${wl}.out
  cd ..
done


# $ACCELSIM_OUT -trace ../llms/QWEN0.6B/traces/kernelslist.g -config $GPGPU_CFG -config $TRACE_CFG > ../llms/QWEN0.6B/QWEN0.6B.out

# file /root/Repos/shared/accel-sim-framework/gpu-simulator/bin/release/accel-sim.out 

gdb --args /root/Repos/shared/accel-sim-framework/gpu-simulator/bin/release/accel-sim.out  -trace /root/Repos/shared/accel-sim-framework/hw_run/traces/device-0/12.8/backprop-rodinia-2.0-ft/4096___data_result_4096_txt/traces/kernelslist.g -config /root/Repos/shared/accel-sim-framework/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM86_RTX3070/gpgpusim.config -config /root/Repos/shared/accel-sim-framework/gpu-simulator/configs/tested-cfgs/SM86_RTX3070/trace.config 

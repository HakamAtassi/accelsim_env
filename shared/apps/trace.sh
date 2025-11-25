
#!/usr/bin/env bash

# source the environment (quote the path)
# (this was in your original script)
#source "$ACCELSIM_FRAMEWORK/gpu-simulator/setup_environment.sh"

export ACCELSIM_FRAMEWORK=/root/Repos/shared/accel-sim-framework
export ACCELSIM_DATA=/accel-sim
export TRACE_DIR=/root/accel-sim-traces

export ACCELSIM_OUT=$ACCELSIM_FRAMEWORK/gpu-simulator/bin/release/accel-sim.out
export GPGPU_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM86_RTX3070/gpgpusim.config
export TRACE_CFG=$ACCELSIM_FRAMEWORK/gpu-simulator/configs/tested-cfgs/SM86_RTX3070/trace.config
export APPS=$ACCELSIM_FRAMEWORK/../apps

export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$CUDA_INSTALL_PATH/bin:$PATH
export CUDA_VISIBLE_DEVICES=0



dir="$ACCELSIM_DATA/gpu-app-collection/bin/12.8/release"


workloads=(
cutlass_00_basic_gemm
cutlass_05_batched_gemm
cutlass_35_gemm_softmax
cutlass_05_batched_gemm
#cutlass_41_fused_multi_head_attention_backward
#cutlass_41_fused_multi_head_attention_fixed_seqlen
#cutlass_41_fused_multi_head_attention_variable_seqlen
pagerank
pagerank_spmv
mem_bw
polybench-*
)


for item in ${workloads[@]}; do
    # intentionally unquoted so shell expands globs like lonestar-* if present
    file=$dir/$item
    for _file in ${file[@]}; do
        saved_pwd=$(pwd)

        # get the real name after glob expansion
        _file_name=$(basename $_file)

        # create trace folder and enter it
        mkdir -p "$TRACE_DIR/${_file_name}"
        cd "$TRACE_DIR/${_file_name}"

        printf '\n'
        printf 'Running %s' "LD_PRELOAD=$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/tracer_tool.so $_file\n"

        LD_PRELOAD=$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/tracer_tool.so $_file

        # return to previous directory
        cd $saved_pwd
    done
done



#LD_PRELOAD=$ACCELSIM_FRAMEWORK/util/tracer_nvbit/tracer_tool/tracer_tool.so $ACCELSIM_DATA/gpu-app-collection/bin/12.8/release/XSBench





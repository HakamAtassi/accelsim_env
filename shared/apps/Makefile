WORKLOAD_NAME ?= bfs

WORKLOAD := $(WORKLOAD_NAME)-rodinia-2.0-ft
OUTDIR := rodinia/$(WORKLOAD)



# Makefile for running Rodinia workloads via accel-sim
.PHONY: all build rodinia_workloads run-rodinia-benchmark run-rodinia-all $(patsubst %,run-%,$(WORKLOADS))

# list of rodinia workloads (no trailing slashes)
WORKLOADS = \
	backprop \
	bfs \
	hotspot \
	heartwall \
	lud \
	nn \
	nw \
	pathfinder \
	srad_v2 \
	streamcluster

all: build

# build simulator
build:
	bash source.sh
	@echo "Building accel-sim (gpu-simulator)..."
	make -j12 -C $(ACCELSIM_FRAMEWORK)/gpu-simulator/


run:
	mkdir -p $(OUTDIR); \
	cd $(OUTDIR) && \
	kernelslist_g=$$(find "$(ACCELSIM_FRAMEWORK)/hw_run/traces/device-0/12.8/$(WORKLOAD)" -type f -name kernelslist.g -print -quit); \
	if [ -z "$$kernelslist_g" ]; then \
	  echo "kernelslist.g not found under $(ACCELSIM_FRAMEWORK)/hw_run/traces/..."; \
	  exit 1; \
	fi; \
	"$(ACCELSIM_OUT)" -trace "$$kernelslist_g" -config $(GPGPU_CFG) -config $(TRACE_CFG) > "$(WORKLOAD).out";



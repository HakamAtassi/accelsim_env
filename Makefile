CONTAINER_NAME := $(notdir $(CURDIR))

dir = $(shell pwd)

# Host HF cache — bind-mounted read-write so models don't need re-downloading.
HF_CACHE ?= $(HF_HOME)
ifeq ($(strip $(HF_CACHE)),)
    HF_CACHE := $(HOME)/.cache/huggingface
endif

run: # create + run docker container (one-time; use `make start` afterwards)
	docker run -it \
		--gpus all --runtime=nvidia \
		--name $(CONTAINER_NAME) \
		-v $(dir)/shared:/workspace \
		-v $(HF_CACHE):/hf_cache \
		-e HF_HOME=/hf_cache \
		-e HF_TOKEN=$(HF_TOKEN) \
		-e USER=$(shell id -un) \
		-e HOME=/workspace \
		--user $(shell id -u):0 \
		ghcr.io/accel-sim/accel-sim-framework:Ubuntu-24.04-cuda-12.8

start:
	docker start -ai $(CONTAINER_NAME)

recreate: # drop the container and re-run with current mounts/env
	-docker rm -f $(CONTAINER_NAME)
	$(MAKE) run


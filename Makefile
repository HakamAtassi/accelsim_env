CONTAINER_NAME=accelsim_env

dir = $(shell pwd)

run: # run docker container. Name it vllm_benchmarks
	sudo docker run -it \
		--gpus all --runtime=nvidia\
		--name $(CONTAINER_NAME) \
		-v $(dir)/shared:/root/Repos/shared \
		ghcr.io/accel-sim/accel-sim-framework:Ubuntu-24.04-cuda-12.8

start: 
	sudo docker start -ai $(CONTAINER_NAME)

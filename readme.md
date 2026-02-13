
# Setup

This repo helps bootstrap an accelsim env. 

## Dependancies

To get started, ensure you have all the required dependancies to use accelsim in a Docker container. Run:

```
sudo apt update &&
sudo apt-get install -y wget build-essential xutils-dev bison zlib1g-dev flex \
      libglu1-mesa-dev git g++ libssl-dev libxml2-dev libboost-all-dev git g++ \
      libxml2-dev vim python3-pip

pip3 install pyyaml plotly psutil
```

## Env Setup

First, you need to ensure you have docker installed. DO NOT INSTALL DOCKER AS A SNAP. Otherwise, you will encounter all sorts of really hard to debug issues. Follow [the official guide](https://docs.docker.com/engine/install/ubuntu). 


Now, set up the current repo. Run:

`https://github.com/HakamAtassi/accelsim_env.git && cd accelsim_env`

Now you need to decide if you intend to develop using a fork of accelsim and gpgpu-sim. This is useful if you want a safe place to keep your code. If you do, read `host_init.py` and update the links as neccesary. Otherwise, proceed to the next step(s).

To pull repos, run:

`python3 host_init.py --use-fork` based on if you plan on using forks or not.

Now you have everything you need in the `shared/` dir. This will be your dev environment. You can modify the code in `shared` as it will be mounted in the docker container. To build the docker container, run:

`make run`

This will build a docker container from the official accel-sim repository. It may take a while to pull everything in. Note: you only ever run "make run" once. This will init a container with the same name as the current dir 'accelsim_env', but as a docker container. After this initial `make run`, you should use `make start` to re-launch your container. 


Finally, in `shared`, you have `init.sh`. This bash script contains a series of bash commands that you should copy paste into your docker terminal. Following this should result in a built version of accel-sim as well as a few traced examples that you should be able to run. I may have missed a few steps (init.sh may skip a few things), but the important steps are:

- Build accelsim
- Create traces of vector-add, rodinia, etc...
- Run them on accel-sim

I remember having issues with their job manager, so I would suggest running accel-sim yourself. 



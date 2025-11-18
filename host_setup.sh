
# feel free to create any forks of things here...




# Clone Accel-Sim framework
git clone git@github.com:HakamAtassi/accel-sim-framework.git shared/accel-sim-framework
cd shared/accel-sim-framework
git checkout 3c96d32
cd ../..

# Clone GPGPU-Sim distribution inside the framework
git git@github.com:HakamAtassi/gpgpu-sim_distribution.git hared/accel-sim-framework/gpu-simulator/gpgpu-sim
cd shared/accel-sim-framework/gpu-simulator/gpgpu-sim
git checkout b18ee39
cd ../../../../


# git clone https://github.com/accel-sim/gpu-app-collection.git shared/accel-sim-framework/gpu-app-collection # not needed if you have the official docker. 


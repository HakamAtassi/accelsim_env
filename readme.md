
# Setup

Accel-sim has a fairly annoying set up process. In order to get up and running, you will likely encouter a few issues that may result from an unset env variable causing the clone of the wrong repo, or an env variable being set that should no longer be set, and variety of other issues that are really annoying to debug. This repo helps streamline this process. 

# Instructions
To get up and running:
- Build the official accel-sim docker container with cuda 12.8 and ubuntu 24.04. 
- Open a terminal and run `bash host_stepup.sh`. This will pull the neccesary repos locally, which will later be mounted to your docker container for their execution. They pull compatibile versions of accel-sim and gpgpu-sim. If you have forks of these, it is your responsibiltiy to make the neccesary changes to this process. If not, proceed to the next step. (We clone these ourselves because accelsim tends to pull in versions that may be in conflict, which causes build issuse, we clone these ourselves to stop accelsim from doing that).
- Run make run (only do this when running for the first time). This wills spin up your docker container. 
- Next, you want to start executing the commands in `shared/init.sh`. This will basically install nvbit, gpgpusim, trace a few things, and also validate the setup.
- If you are able to run both ptx and sass simulations, congrats, your environment is set up. 
- Make sure you read the init.sh as it contains instructions on how to run the commands. 



Note: Towards the end of the set up process, when you run the SASS trace, you need to collect the trace using a system with the same GPU archtiecture as what you are simulating. I have an ampere GPU, so I set the variable to a RTX3070. 

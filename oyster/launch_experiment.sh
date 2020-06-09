#!/bin/bash

export PYTHONPATH=./rand_param_envs:$PYTHONPATH

python launch_experiment.py ./configs/cheetah_vel.json

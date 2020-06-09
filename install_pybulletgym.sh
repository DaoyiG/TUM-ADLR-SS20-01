#!/bin/bash

conda activate pearl

git clone https://github.com/benelot/pybullet-gym.git
cd pybullet-gym
pip install -e .

conda deactivate

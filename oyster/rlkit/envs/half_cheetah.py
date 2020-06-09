import numpy as np
#from gym.envs.mujoco import HalfCheetahEnv as HalfCheetahEnv_
from pybulletgym.envs.roboschool.envs.locomotion.half_cheetah_env import HalfCheetahBulletEnv as HalfCheetahEnv_

class HalfCheetahEnv(HalfCheetahEnv_):
    def __init__(self):
        pass
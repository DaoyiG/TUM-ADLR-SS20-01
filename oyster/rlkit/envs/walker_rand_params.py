import numpy as np
from pybullet_envs.gym_locomotion_envs import Walker2DBulletEnv as Walker2DEnv
from .rand_params_base import RandParamsEnv

from . import register_env

@register_env('walker-rand-params')
class WalkerRandParamsWrappedEnv(RandParamsEnv,Walker2DEnv):
    def __init__(self, n_tasks=2, randomize_tasks=True):
        # super(WalkerRandParamsWrappedEnv, self).__init__()
        # super(WalkerRandParamsWrappedEnv, self).__init__()
        # self.tasks = self.sample_tasks(n_tasks)
        # self.rand_params = ['body_mass', 'dof_damping', 'body_inertia', 'geom_friction']
        # self.reset_task(0)
        # TODO

import numpy as np
from pybullet_envs.gym_locomotion_envs import Walker2DBulletEnv as Walker2DEnv
import pybullet as p

from .rand_params_base import RandParamsEnv

from . import register_env

@register_env('walker-rand-params')
class WalkerRandParamsEnv(Walker2DEnv):
    def __init__(self, n_tasks=2, randomize_tasks=True):
        super(WalkerRandParamsEnv, self).__init__()
        self.reset()
        self.tasks = self.sample_tasks(n_tasks)
        self.rand_params = ['mass']
        # self.rand_params = ['body_mass', 'dof_damping', 'body_inertia', 'geom_friction']
        self.reset_task(0)

    def get_all_task_idx(self):
        return range(len(self.tasks))

    def reset_task(self, idx):
        self._task = self.tasks[idx]
        self._goal = idx
        print("task:", self._task)
        self.set_task(self._task)
        self.reset()

    def set_task(self, task):
        """
                Sets the specified task to the current environment
                Args:
                    task: task of the meta-learning environment
        """
        # use pybullet API to change the attr
        for param, param_val in task.items():
            # param_variable = getattr(self.model, param)
            # assert param_variable.shape == param_val.shape, 'shapes of new parameter value and old one must match'
            # setattr(self.model, param, param_val)
            part = self.robot.robot_body
            bodyUniqueId = part.bodies[part.bodyIndex]
            partIndex = part.bodyPartIndex
            p.changeDynamics(bodyUniqueId, partIndex, **{param: param_val})
        self.cur_params = task

    def sample_tasks(self, num_tasks):
        """
        Samples task of the meta-environment

        Args:
            num_tasks (int) : number of different meta-tasks needed

        Returns:
            tasks (list) : an (n_tasks) length list of tasks
        """
        # body_mass -> one multiplier for all body parts
        # body_inertia
        # dof_damping -> different multiplier for different dofs/joints
        # geom_friction -> friction at the body components

        # get the original parameter
        part = self.robot.robot_body
        bodyUniqueId = part.bodies[part.bodyIndex]
        partIndex = part.bodyPartIndex
        info = p.getDynamicsInfo(bodyUniqueId, partIndex)
        original_mass = info[0]
        original_lateral_friction = info[1]
        original_body_inertia = info[2]
        original_contact_damping = info[-4]

        tasks = []
        for _ in range(num_tasks):
            tasks_params = {}

            # "additive noise" to the original parameters
            mass = original_mass + np.random.uniform(0.0, 3.0)
            lateral_friction = original_lateral_friction * np.random.uniform(0.8, 1.2)
            # localInertiaDiagnoal = original_body_inertia * np.random.uniform(0.8, 1.2, 3)
            contact_damping = original_contact_damping * np.random.uniform(0.8, 1.2)
            tasks_params['mass'] = mass
            tasks_params['lateralFriction'] = lateral_friction
            # tasks_params['localInertiaDiagnoal'] = localInertiaDiagnoal
            tasks_params['contactDamping'] = contact_damping
            tasks.append(tasks_params)

        return tasks
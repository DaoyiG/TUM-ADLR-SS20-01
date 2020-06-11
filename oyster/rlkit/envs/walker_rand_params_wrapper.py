import numpy as np
# from rand_param_envs.walker2d_rand_params import Walker2DRandParamsEnv

from . import register_env
# from pybulletgym.envs.roboschool.envs.locomotion.walker2d_env import Walker2DBulletEnv as Walker2DRandParamsEnv
# from pybulletgym.envs.mujoco.envs.locomotion.walker2d_env import Walker2DMuJoCoEnv as Walker2DRandParamsEnv
from pybullet_envs.gym_locomotion_envs import Walker2DBulletEnv as Walker2DRandParamsEnv

@register_env('walker-rand-params')
class WalkerRandParamsWrappedEnv(Walker2DRandParamsEnv):
    # def __init__(self, n_tasks=2, randomize_tasks=True):
    #     super(WalkerRandParamsWrappedEnv, self).__init__()
    #     self.tasks = self.sample_tasks(n_tasks)
    #     self.rand_params = ['body_mass', 'dof_damping', 'body_inertia', 'geom_friction']
    #     self.reset_task(0)

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

        # for param, param_val in task.items():
        #     param_variable = getattr(self.model, param)
        #     assert param_variable.shape == param_val.shape, 'shapes of new parameter value and old one must match'
        #     setattr(self.model, param, param_val)
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
        np.random.seed(1337)

        tasks = []
        for _ in range(num_tasks):
            tasks_params = {}

            # TODO: values need to be tuned
            mass = np.random.uniform(0.0, 3.0)
            body_inertia = np.random.uniform(0.0, 3.0)
            dof_damping = np.random.uniform(0.0, 3.0)
            geom_friction = np.random.uniform(0.0, 3.0)
            tasks_params['body_mass'] = mass
            tasks_params['body_inertia'] = body_inertia
            tasks_params['dof_damping'] = dof_damping
            tasks_params['geom_friction'] = geom_friction
            tasks.append(tasks_params)

        return tasks

    # from RandomEnv
    # def sample_tasks(self, n_tasks):
    #
    #     param_sets = []
    #
    #     for _ in range(n_tasks):
    #         # body mass -> one multiplier for all body parts
    #
    #         new_params = {}
    #
    #         if 'body_mass' in self.rand_params:
    #             body_mass_multiplyers = np.array(1.5) ** np.random.uniform(-self.log_scale_limit, self.log_scale_limit,  size=self.model.body_mass.shape)
    #             new_params['body_mass'] = self.init_params['body_mass'] * body_mass_multiplyers
    #
    #         # body_inertia
    #         if 'body_inertia' in self.rand_params:
    #             body_inertia_multiplyers = np.array(1.5) ** np.random.uniform(-self.log_scale_limit, self.log_scale_limit,  size=self.model.body_inertia.shape)
    #             new_params['body_inertia'] = body_inertia_multiplyers * self.init_params['body_inertia']
    #
    #         # damping -> different multiplier for different dofs/joints
    #         if 'dof_damping' in self.rand_params:
    #             dof_damping_multipliers = np.array(1.3) ** np.random.uniform(-self.log_scale_limit, self.log_scale_limit, size=self.model.dof_damping.shape)
    #             new_params['dof_damping'] = np.multiply(self.init_params['dof_damping'], dof_damping_multipliers)
    #
    #         # friction at the body components
    #         if 'geom_friction' in self.rand_params:
    #             dof_damping_multipliers = np.array(1.5) ** np.random.uniform(-self.log_scale_limit, self.log_scale_limit, size=self.model.geom_friction.shape)
    #             new_params['geom_friction'] = np.multiply(self.init_params['geom_friction'], dof_damping_multipliers)
    #
    #         param_sets.append(new_params)
    #
    #     return param_sets
    def save_parameters(self):
        pass

    # def save_parameters(self):
    #     self.init_params = {}
    #     if 'body_mass' in self.rand_params:
    #         self.init_params['body_mass'] = self.model.body_mass
    #
    #     # body_inertia
    #     if 'body_inertia' in self.rand_params:
    #         self.init_params['body_inertia'] = self.model.body_inertia
    #
    #     # damping -> different multiplier for different dofs/joints
    #     if 'dof_damping' in self.rand_params:
    #         self.init_params['dof_damping'] = self.model.dof_damping
    #
    #     # friction at the body components
    #     if 'geom_friction' in self.rand_params:
    #         self.init_params['geom_friction'] = self.model.geom_friction
    #     self.cur_params = self.init_params
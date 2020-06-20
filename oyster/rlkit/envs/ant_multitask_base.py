import numpy as np

from pybullet_envs.gym_locomotion_envs import AntBulletEnv as AntEnv

class MultitaskAntEnv(AntEnv):
    def __init__(self, task={}, n_tasks=2, **kwargs):
        self._task = task
        self.tasks = self.sample_tasks(n_tasks)
        self._goal = self.tasks[0]['goal']
        super(MultitaskAntEnv, self).__init__(**kwargs)

    def get_all_task_idx(self):
        return range(len(self.tasks))

    def reset_task(self, idx):
        self._task = self.tasks[idx]
        self._goal = self._task['goal'] # assume parameterization of task by single vector
        self.reset()

    # might need/ or not
    # def reset_model(self):
    #     qpos = [0,0,0.45] + self.np_random.uniform(size=3, low=-.1, high=.1)
    #     self.robot.robot_body.reset_position(qpos)
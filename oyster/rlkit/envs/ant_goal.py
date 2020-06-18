import numpy as np

from rlkit.envs.ant_multitask_base import MultitaskAntEnv
from . import register_env


# Copy task structure from https://github.com/jonasrothfuss/ProMP/blob/master/meta_policy_search/envs/mujoco_envs/ant_rand_goal.py
@register_env('ant-goal')
class AntGoalEnv(MultitaskAntEnv):
    def __init__(self, task={}, n_tasks=2, randomize_tasks=True, **kwargs):
        super(AntGoalEnv, self).__init__(task, n_tasks, **kwargs)

    """
    # original pearl
    # def step(self, action):
    #     self.do_simulation(action, self.frame_skip)
    #     xposafter = np.array(self.get_body_com("torso"))
    #
    #     goal_reward = -np.sum(np.abs(xposafter[:2] - self._goal)) # make it happy, not suicidal
    #
    #     ctrl_cost = .1 * np.square(action).sum()
    #     contact_cost = 0.5 * 1e-3 * np.sum(
    #         np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))
    #     survive_reward = 0.0
    #     reward = goal_reward - ctrl_cost - contact_cost + survive_reward
    #     state = self.state_vector()
    #     done = False
    #     ob = self._get_obs()
    #     return ob, reward, done, dict(
    #         goal_forward=goal_reward,
    #         reward_ctrl=-ctrl_cost,
    #         reward_contact=-contact_cost,
    #         reward_survive=survive_reward,
    #     )
    """

    def step(self, action):
        # Use original step function
        observation, reward, done, _ = super(AntGoalEnv, self).step(action)

        xposafter = self._get_obs()

        goal_reward = -np.sum(np.abs(xposafter[:2] - self._goal))  # make it happy, not suicidal

        # ctrl_cost = .1 * np.square(action).sum()
        ctrl_cost = 0.0

        # TODO: need to find how to get this external force in here and _get_obs()
        # contact_cost = 0.5 * 1e-3 * np.sum(
        #     np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))

        contact_cost = 0.0
        survive_reward = 0.0
        reward = goal_reward - ctrl_cost - contact_cost + survive_reward

        done = False
        # TODO: may have problem here, the original pearl use ob = self._get_obs(), but now the dim is not match
        return observation, reward, done, dict(
            goal_forward=goal_reward,
            reward_ctrl=-ctrl_cost,
            reward_contact=-contact_cost,
            reward_survive=survive_reward,
        )
        # infos = dict(reward_forward=reward, reward_ctrl=-ctrl_cost, task=self._task)
        # return (observation, reward, done, infos)

    # moved to the multiclass base
    def sample_tasks(self, num_tasks):
        a = np.random.random(num_tasks) * 2 * np.pi
        r = 3 * np.random.random(num_tasks) ** 0.5
        goals = np.stack((r * np.cos(a), r * np.sin(a)), axis=-1)
        tasks = [{'goal': goal} for goal in goals]
        return tasks

    # from original pearl
    # def _get_obs(self):
    #     return np.concatenate([
    #         self.sim.data.qpos.flat,
    #         self.sim.data.qvel.flat,
    #         np.clip(self.sim.data.cfrc_ext, -1, 1).flat,
    #     ])
    def _get_obs(self):
        return np.concatenate([
            self.robot.robot_body.pose().xyz(),
            self.robot.robot_body.speed(),
        ]).astype(np.float32).flatten()

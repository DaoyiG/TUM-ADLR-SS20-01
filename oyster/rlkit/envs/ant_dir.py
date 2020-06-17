import numpy as np

from rlkit.envs.ant_multitask_base import MultitaskAntEnv
from . import register_env


@register_env('ant-dir')
class AntDirEnv(MultitaskAntEnv):

    def __init__(self, task={}, n_tasks=2, forward_backward=False, randomize_tasks=True, observation_noise=0, **kwargs):
        self.forward_backward = forward_backward
        self._observation_noise = observation_noise
        super(AntDirEnv, self).__init__(task, n_tasks, **kwargs)

    def step(self, action):
        # torso_xyz_before = np.array(self.get_body_com("torso"))
        torso_xyz_before = self._get_obs()
        direct = (np.cos(self._goal), np.sin(self._goal))

        # self.do_simulation(action, self.frame_skip)
        observation, reward, done, _ = super(AntDirEnv, self).step(action)

        if self._observation_noise > 1e-8:
            noise = self._observation_noise * np.random.randn(self.observation_space.shape[0])
            observation += noise

        # torso_xyz_after = np.array(self.get_body_com("torso"))
        torso_xyz_after = self._get_obs()

        torso_velocity = torso_xyz_after - torso_xyz_before
        forward_reward = np.dot((torso_velocity[:2] / (1. / 240.)), direct)

        ctrl_cost = .5 * np.square(action).sum()
        # contact_cost = 0.5 * 1e-3 * np.sum(
        #     np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))
        contact_cost = 0.0
        survive_reward = 1.0
        reward = forward_reward - ctrl_cost - contact_cost + survive_reward

        state = self.state_vector()
        notdone = np.isfinite(state).all() \
                  and state[2] >= 0.2 and state[2] <= 1.0
        done = not notdone

        # TODO: may need to modify _get_obs() to solve the dim problem
        # ob = self._get_obs()
        return observation, reward, done, dict(
            reward_forward=forward_reward,
            reward_ctrl=-ctrl_cost,
            reward_contact=-contact_cost,
            reward_survive=survive_reward,
            torso_velocity=torso_velocity,
        )

    def sample_tasks(self, num_tasks):
        if self.forward_backward:
            assert num_tasks == 2
            velocities = np.array([0., np.pi])
        else:
            velocities = np.random.uniform(0., 2.0 * np.pi, size=(num_tasks,))
        tasks = [{'goal': velocity} for velocity in velocities]
        return tasks

    def _get_obs(self):

        return np.concatenate([
            self.robot.robot_body.pose().xyz(),
            self.robot.robot_body.speed(),
        ]).astype(np.float32).flatten()

    # modified from gym
    def state_vector(self):
        return np.concatenate([
            self.robot.robot_body.pose().xyz(),
            self.robot.robot_body.speed(),
        ])
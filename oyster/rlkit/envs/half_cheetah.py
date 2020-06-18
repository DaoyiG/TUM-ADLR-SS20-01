import numpy as np
from pybullet_envs.gym_locomotion_envs import HalfCheetahBulletEnv as HalfCheetahEnv_


class HalfCheetahEnv(HalfCheetahEnv_):

    # get obs returns observations
    def _get_obs(self):
        # return np.concatenate([
        #     self.sim.data.qpos.flat[1:],
        #     self.sim.data.qvel.flat,
        #     self.get_body_com("torso").flat,
        # ]).astype(np.float32).flatten()

        return np.concatenate([
            self.robot.robot_body.pose().xyz(),
            self.robot.robot_body.speed(),
            #TODO: what is torso?
            #self.get_body_com("torso").flat,
        ]).astype(np.float32).flatten()

    @property
    def get_pose_xyz(self):
        return self.robot.robot_body.pose().xyz()

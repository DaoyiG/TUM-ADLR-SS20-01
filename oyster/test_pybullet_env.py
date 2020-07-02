import time
import gym  # open ai gym
import pybullet  
import pybullet_envs  # register PyBullet enviroments with open ai gym

#env = gym.make('MinitaurBulletEnv-v0',render=True) 
env = gym.make('AntBulletEnv-v0')
env.render()
env.reset()  # should return a state vector if everything worked
time.sleep(1)

for i in range(1000):
	obs, rewards, done, _ = env.step(env.action_space.sample())
	#env.render()
	time.sleep(0.05)



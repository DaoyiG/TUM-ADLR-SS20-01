import gym  # open ai gym
import pybullet as p
import pybullet_envs  # register PyBullet enviroments with open ai gym

env = gym.make('HalfCheetahBulletEnv-v0')
# p is the pybullet package
# important: must reset so that env has the true robot object!
env.reset()
# part can be either parts['torso'] or robot_body
part = env.robot.parts['torso']
part = env.robot.robot_body
print("parts = ", part)
bodyUniqueId = part.bodies[part.bodyIndex]
partIndex = part.bodyPartIndex
info = p.getDynamicsInfo(bodyUniqueId, partIndex)
print("DynamicsInfo: ", info)
print('before mass', info[0])
p.changeDynamics(bodyUniqueId, partIndex, mass=5)
info = p.getDynamicsInfo(bodyUniqueId, partIndex)
print('after mass', info[0])

# Reference code from an awesome answer
# https://github.com/bulletphysics/bullet3/issues/1873

# import gym
# import pybullet_envs
# print("1")
# env = gym.make('HalfCheetahBulletEnv-v0')
# #env = gym.make("InvertedPendulumBulletEnv-v0")
#
# #env.render(mode="human")
# print("2")
#
# unwrapped = env.unwrapped
# print("2a")
# unwrapped.reset()
# print("2b")
# p = unwrapped._p
# print("3")
# print("parts = ", unwrapped.robot.parts['torso'])
#
# part = unwrapped.robot.parts['torso']
# print("numBodies = ", p.getNumBodies())
# for b in range (p.getNumBodies()):
# 	print("info for body[",b,"]=",p.getBodyInfo(b))
# 	for j in range(p.getNumJoints(b)):
# 		print("bodyInfo[",b,",",j,"]=",p.getJointInfo(b,j))
#
# bodyIndex = part.bodyIndex
# bodyUniqueId = part.bodies[bodyIndex]
# print("bodyUniqueId=", bodyUniqueId)
# numJoints = p.getNumJoints(bodyIndex)
# print("numJoints=",numJoints)
#
# partIndex = 2#part.bodyPartIndex
# info = p.getDynamicsInfo(part.bodies[bodyIndex], partIndex)
# print('before mass', info[0])
# print("bodyIndex = ", bodyIndex)
# print("partIndex = ", partIndex)
# p.changeDynamics(part.bodies[bodyIndex], partIndex, mass=2)
# info = p.getDynamicsInfo(part.bodies[bodyIndex], partIndex)
# print('after mass', info[0])
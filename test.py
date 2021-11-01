import env_homework

env = env_homework.cleanerEnv()

obs = env.reset()
env.render()
print(obs)
for _ in range(10):
    action = 0
    obs, reward, done, info = env.step(action)
    print(obs)
    print(reward)
    print("")
    env.render()
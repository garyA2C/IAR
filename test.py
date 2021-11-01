import env_homework
import matplotlib.pyplot as plt

env = env_homework.cleanerEnv()

UPDATE_EVERY = 100
EPISODE = 10000

all_rewards = []
metrics = {'ep': [], 'avg': [], 'min': [], 'max': []}

for episode in range(EPISODE):
    episode_reward = 0
    action = 3

    done = False
    obs = env.reset()

    while not done:
        obs, reward, done, info = env.step(action)
        episode_reward += reward
        # print(obs)
        # print("")

        if obs[39] == 2:
            action = 0
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            action = 2

        if action == 2 and obs[41] == 2:
            action = 0
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            action = 3

    all_rewards.append(episode_reward)
    if episode % UPDATE_EVERY == 0:
        latestEpisodes = all_rewards[-UPDATE_EVERY:]
        averageCnt = sum(latestEpisodes) / len(latestEpisodes)
        metrics['ep'].append(episode)
        metrics['avg'].append(averageCnt)
        metrics['min'].append(min(latestEpisodes))
        metrics['max'].append(max(latestEpisodes))
        print("Run:", episode, "Average:", averageCnt, "Min:", min(latestEpisodes), "Max:",
              max(latestEpisodes))

plt.plot(metrics['ep'], metrics['avg'], label="average rewards")
plt.plot(metrics['ep'], metrics['min'], label="min rewards")
plt.plot(metrics['ep'], metrics['max'], label="max rewards")
plt.legend(loc=4)
plt.show()


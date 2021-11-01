import env_homework
import matplotlib.pyplot as plt
import numpy as np

env = env_homework.cleanerEnv()

LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95

UPDATE_EVERY = 100
EPISODES = 10000

epsilon = 1
START_EPSILON_DECAY = 1
END_EPSILON_DECAY = EPISODES // 2
epsilon_decay_value = epsilon / (END_EPSILON_DECAY - START_EPSILON_DECAY)

couples_rencontre = []

all_rewards = []
metrics = {'ep': [], 'avg': [], 'min': [], 'max': []}


obsSpaceSize = len(env.observation_space.high)
print(obsSpaceSize)
qTable = []
# qTable = np.random.uniform(low=-2, high=0,
#                            size=([numBins] * obsSpaceSize + [env.action_space.n]))

for episode in range(EPISODES):
    episode_reward = 0

    done = False
    returns = {}

    obs = env.reset()
    obs_tuple = tuple(obs)

    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(qTable[obs_tuple])
        else:
            action = np.random.randint(0, env.action_space.n)

        obs, reward, done, info = env.step(action)
        obs_tuple = tuple(obs)
        episode_reward += reward

        if not (obs_tuple + (action,)) in returns.keys():
            returns[obs_tuple + (action,)] = 0
        for key in returns.keys():
            returns[key] += reward

    # After the episode
    # Update qTable
    for key in returns.keys():
        qTable[key] = (qTable[key] * (episode - 1) + returns[key]) / episode

    # Update epsilon
    if END_EPSILON_DECAY >= episode >= START_EPSILON_DECAY:
        epsilon -= epsilon_decay_value

    # add the reward of the episode the reward list
    all_rewards.append(episode_reward)

    # Metrics
    if episode % UPDATE_EVERY == 0:
        latestEpisodes = all_rewards[-UPDATE_EVERY:]
        averageCnt = sum(latestEpisodes) / len(latestEpisodes)
        metrics['ep'].append(episode)
        metrics['avg'].append(averageCnt)
        metrics['min'].append(min(latestEpisodes))
        metrics['max'].append(max(latestEpisodes))
        print("Run:", episode, "Average:", averageCnt, "Min:", min(latestEpisodes), "Max:",
              max(latestEpisodes))

# Plot the metrics at the end of the execution
plt.plot(metrics['ep'], metrics['avg'], label="average rewards")
plt.plot(metrics['ep'], metrics['min'], label="min rewards")
plt.plot(metrics['ep'], metrics['max'], label="max rewards")
plt.legend(loc=4)
plt.show()


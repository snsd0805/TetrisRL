from enviroment import TetrisEnviroment
from agent import TetrisRLAgent
import torch
import torch.nn.functional as F
from enviroment import TetrisEnviroment
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("use:", device)

PATH = "model.h5"

def showGame(views:list, reward:int, score:int, completeLines:int) -> None:
    for i in range(20):
        print(str(i).rjust(2), end=' ')
        for j in range(10):
            if views[i][j]:
                print('■', end='')
            else:
                print('□', end='')
        print()
    print("reward:", reward)
    print("total_reward:", score)
    print("total_line  :", completeLines)
    print()


env = TetrisEnviroment()
agent = TetrisRLAgent(device)

avgTotalRewards = []
for batch in range(100000):

    log_probs, rewards = [], []
    total_rewards = []

    for episode in range(5):
        total_reward = 0
        total_lines = 0

        pixel, reward, done, info = env.reset()
        while 1:
            showGame(pixel, reward, total_reward, total_lines)

            pixel = torch.tensor(pixel, dtype=torch.float32)
            blockType = F.one_hot(torch.tensor(info[2]), 7)
            blockLoc  = torch.tensor(info[:2], dtype=torch.float32)
            observation = torch.cat([pixel.reshape(-1), blockLoc, blockType], dim=0)
            observation = observation.to(device)

            action, log_prob = agent.sample(observation)
            pixel, reward, done, info = env.step(action)
            rewards.append(reward)
            log_probs.append(log_prob)
            total_reward += reward
            total_lines += info[3]
            if done:
                total_rewards.append(total_reward)
                break
    
    print("TOTAL REWARDS", total_rewards)
    avgTotalReward = sum(total_rewards) / len(total_rewards)
    avgTotalRewards.append(avgTotalReward)

    ALPHA = 0.98
    delayRewards = []
    for start in range(len(rewards)):
        ans = rewards[start]
        weight = ALPHA
        for i in range(start+1, len(rewards)):
            ans += (weight * rewards[i])
            weight *= ALPHA
        delayRewards.append(ans)

    rewards = torch.tensor(delayRewards)
    log_probs = torch.stack(log_probs)

    print(batch)
    print(rewards.shape)
    print(log_probs.shape)
    print(avgTotalReward)
    # print(rewards.tolist())

    agent.learn(rewards, log_probs)
    # time.sleep(5)

agent.save(PATH)
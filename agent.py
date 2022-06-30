import torch
from torch.optim import Adam
from torch.distributions import Categorical
from zmq import device
from enviroment import TetrisEnviroment
from network import TetrisRLModel
import torch.nn.functional as F

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("use:", device)

PATH = "model.h5"

class TetrisRLAgent():
    def __init__(self) -> None:
        self.model = TetrisRLModel()
        self.model = self.model.to(device)
        self.optim = Adam(self.model.parameters(), lr=0.001)
    
    def sample(self, observation):
        action_prob = self.model(observation)
        action_dist = Categorical(action_prob)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)
        return action, log_prob
    
    def learn(self, rewards, log_probes):
        rewards = rewards.to(device)
        loss = ((-log_probes * rewards)).sum()

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
    
    def save(self, PATH): # You should not revise this
        Agent_Dict = {
            "network" : self.network.state_dict(),
            "optimizer" : self.optimizer.state_dict()
        }
        torch.save(Agent_Dict, PATH)

def showGame(views:list, score:int) -> None:
    for i in range(20):
        print(str(i).rjust(2), end=' ')
        for j in range(10):
            if views[i][j]:
                print('■', end='')
            else:
                print('□', end='')
        print()
    print("Score:", score)
    print()

env = TetrisEnviroment()
agent = TetrisRLAgent()

avgTotalRewards = []
for batch in range(100000):

    log_probs, rewards = [], []
    total_rewards = []

    for episode in range(5):
        total_reward = 0

        pixel, reward, done, info = env.reset()
        while 1:
            showGame(pixel, total_reward)

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
            if done:
                total_rewards.append(total_reward)
                break
    
    avgTotalReward = sum(total_rewards) / len(total_rewards)
    avgTotalRewards.append(avgTotalReward)

    rewards = torch.tensor(rewards)
    log_probs = torch.stack(log_probs)

    print(rewards.shape)
    print(log_probs.shape)

    agent.learn(rewards, log_probs)

agent.save(PATH)
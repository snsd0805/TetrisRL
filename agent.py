import torch
from torch.optim import Adam
from torch.distributions import Categorical
from network import TetrisRLModel

class TetrisRLAgent():
    def __init__(self, device) -> None:
        self.device = device
        self.model = TetrisRLModel()
        self.model = self.model.to(self.device)
        self.optim = Adam(self.model.parameters(), lr=0.001)
    
    def sample(self, observation):
        action_prob = self.model(observation)
        action_dist = Categorical(action_prob)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)
        return action, log_prob
    
    def learn(self, rewards, log_probes):
        rewards = rewards.to(self.device)
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


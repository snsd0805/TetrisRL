import torch
import torch.nn as nn
import torch.nn.functional as F

class TetrisRLModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = nn.Linear(in_features=209, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=32)
        self.fc3 = nn.Linear(in_features=32, out_features=10)
    
    def forward(self, observation):
        observation = observation.to(dtype=torch.float32)
        observation = torch.relu(self.fc1(observation))
        observation = torch.relu(self.fc2(observation))
        observation = F.softmax(self.fc3(observation), dim=0)
        return observation

from playerDummy import PlayerDummy
from world import World
from Players.playerFunctions import selectRandomMove


import random
from collections import deque
import math
import numpy as np
import copy

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, output_size)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, tuple):
        """tuple has to be (state, action, next_state, reward)"""
        self.memory.append(tuple)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQNPlayer(PlayerDummy):
    def __init__(self, name : int, height=10, width=10, nbPlayers=4, nbPenguins=3):
        self.BATCH_SIZE = 128
        self.GAMMA = 0.99        # Discount factor
        self.EPS_START = 0.9
        self.EPS_END = 0.05
        self.EPS_DECAY = 1000
        self.TAU = 0.005         # Target network update rate
        self.LR = 1e-4           # Learning rate

        self.nbPenguins = nbPenguins

        # if gpu is to be used
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.state_space = height*width*2
        self.action_space = 6*10*nbPenguins

        self.name = name
        self.model = DQN(self.state_space, self.action_space).to(self.device).float()
        self.target = DQN(self.state_space, self.action_space).to(self.device).float()
        self.target.load_state_dict(self.model.state_dict())

        self.optimizer = optim.AdamW(self.model.parameters(), lr=self.LR, amsgrad=True)
        self.memory = ReplayMemory(10000)

        self.steps_done = 0

    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def tensorToMove(self, tensor, world: World):
        n = tensor.max(0)[1].view(1, 1).item()
        penguin = n // self.nbPenguins
        n = n % self.nbPenguins
        pos = world.get_pingouin_coordinates(self.name, penguin)
        return (pos, n//10, n%10)

    def chooseMove(self, world: World):
        fgrid, pgrid = world.dataForIA(self.name)
        state = torch.tensor(np.concatenate(fgrid, pgrid, axis=0), dtype=torch.float32, device=self.device)
        eps_threshold = self.EPS_END + (self.EPS_START - self.EPS_END) * math.exp(-1. * self.steps_done / self.EPS_DECAY)
        self.steps_done += 1

        self.world = copy.deepcopy(world)

        if random.random() > eps_threshold:
            with torch.no_grad():
                move = self.tensorToMove(self.model(state.float()), world)
        else:
            playable, movesList = world.possibleMove(self.name)         # Get the possible moves for this player
            if not playable:
                move = None 
            move = selectRandomMove(movesList)
        
        if move not in world.possibleMove(self.name):
            self.memory.push((state, move, None, -400))
        else : 
            previous_points = world.get_point(self.name)
            self.world.move(self.name, move[0], move[1], move[2])   #TODO check if it works
            next_state = self.world.dataForIA(self.name)
            reward = self.world.get_point(self.name) - previous_points
            self.memory.push((state, move, next_state, reward))
        
        return move
    
    def optimize_model(self):
        if len(self.memory) < self.BATCH_SIZE:
            return
        batch = self.memory.sample(self.BATCH_SIZE)

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            [i[2] for i in batch])), device=self.device, dtype=torch.bool)
        non_final_next_states = torch.tensor([s for s in [i[2] for i in batch]
                                                    if s is not None], device=self.device, dtype=torch.float32)
        state_batch = torch.tensor([i[0] for i in batch], device=self.device, dtype=torch.float32)
        action_batch = torch.tensor([i[1] for i in batch], device=self.device, dtype=torch.float32)
        reward_batch = torch.cat([i[3] for i in batch], device=self.device, dtype=torch.float32)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to model
        state_action_values = self.model(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1)[0].
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.BATCH_SIZE, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target(non_final_next_states).max(1)[0]
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.GAMMA) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(self.model.parameters(), 100)
        self.optimizer.step()

        # Soft update of the target network
        target_net_state_dict = self.target.state_dict()
        policy_net_state_dict = self.model.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*self.TAU + target_net_state_dict[key]*(1-self.TAU)
        self.target.load_state_dict(target_net_state_dict)
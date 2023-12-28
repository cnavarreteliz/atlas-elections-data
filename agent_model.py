import numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class ElectionAgent(Agent):
    """ An agent in an election model."""
    def __init__(self, unique_id, model, candidates, p):
        super().__init__(unique_id, model)
        self.choice = np.random.choice(candidates, 1, p=p)

    def step(self):
        pass

class ElectionModel(Model):
    def __init__(self, N=1000, candidates=["A"], p=[1], width=10, height=10) -> None:
        self.num_agents = N
        self.n_candidates = len(candidates)
        self.candidates = candidates
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)

        for i in range(self.num_agents):
            a = ElectionAgent(i, self, candidates=candidates, p=p)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(          
            agent_reporters={"State": "state"})
        
    def step(self):
        """Advance the model by one step."""

        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()
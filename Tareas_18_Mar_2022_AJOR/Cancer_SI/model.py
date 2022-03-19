# Alberto Josué Ortiz Rosales
# 18 feb 2022

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import random 



class CancerAgent(Agent):

    def __init__(self, unique_id,  pos, model, p_crecer, p_evadir):

        self.unique_id= unique_id
        self.pos = pos
        self.model = model
        self.type = 1
        self.prob_crecer= p_crecer
        self.prob_evadir= p_evadir
    
    def neighbors (self):
        list_neigh = []
        x , y = self.pos
        for i in range (-1, 2):
            for j in range(-1,2):
                a = (i+x) %self.model.width
                b = (j+y) %self.model.height
                list_neigh.append((a,b))
        list_neigh.remove((x,y))
        return list_neigh
        

    def step(self):
        r1 = random.random()
        list_empty_neig=self.neighbors()
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            list_empty_neig.remove(neighbor.pos)
        if len(list_empty_neig)>0:
            
            #print(new_position)
            if(self.model.prob_crecer< r1):
                new_position = random.choice(list_empty_neig)
                newCancerCell = CancerAgent(self.model.next_id(), self.pos, self.model, self.prob_crecer, self.prob_evadir)
                self.model.grid.place_agent(newCancerCell, new_position)
                self.model.schedule.add(newCancerCell)
            


class InmuneAgent(Agent):
    def __init__(self,  unique_id, pos, model):
        self.unique_id= unique_id
        self.pos = pos
        self.model = model
        self.type = 0

    def neighbors (self):
        list_neigh = []
        x , y = self.pos
        for i in range (-1, 2):
            for j in range(-1,2):
                a = (i+x) %self.model.width
                b = (j+y) %self.model.height
                list_neigh.append((a,b))
        list_neigh.remove((x,y))
        return list_neigh
        


    def step(self):
        r1 = random.random()
        list_empty_neigh = self.neighbors()
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            list_empty_neigh.remove(neighbor.pos)
            if neighbor.type == 1:
                if r1> neighbor.prob_evadir:
                    self.model.grid.remove_agent(neighbor)
                    self.model.schedule.remove(neighbor)
            # if neighbor.pos is not None:
            #     if self.model.grid.is_cell_empty(neighbor.pos):
            #         list_empty.append(neighbor.pos)

        
        if len(list_empty_neigh)>0:
            new_position = random.choice(list_empty_neigh)
            #print(new_position)
            self.model.grid.move_agent(self, new_position)
        


class Ising(Model):
    """
    Model class for the Ising model.
    """

    def __init__(self, height=50, width=50, minority_pc=0.5, density=0.4, prob_crecer=0.5, prob_evadir=0.5):
        """ """

        self.height = height
        self.width = width
        self.minority_pc = minority_pc
        self.density = density
        self.total_energy =0
        self.prob_crecer = prob_crecer
        self.prob_evadir = prob_evadir
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)
        
        self.current_id =0
        self.datacollector = DataCollector(
            {"energy": "energy"}, 
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        i=0
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            position= (x,y)
            if self.random.random() < self.density:
                id=self.next_id()
                if self.random.random() < self.minority_pc:
                    agent = CancerAgent( id, (x,y), self, self.prob_crecer, self.prob_evadir)
                else:
                    agent = InmuneAgent( id, (x,y), self)

                self.grid.position_agent(agent, (x,y))
                self.schedule.add(agent)
            i+=1
        self.running = True
        self.datacollector.collect(self)

    

    def step(self):

        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.total_energy == self.schedule.get_agent_count():
            self.running = False


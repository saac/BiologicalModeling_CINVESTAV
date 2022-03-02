# Alberto Josué Ortiz Rosales
# 28 feb 2022
# Modelo de ISING utilizando el algoritmo Metropolis
# Versión 2 
# se mejora las u1 y u2 al hacerlas directamente normales o uniformes.


from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import random 

class IsingAgent(Agent):

    def __init__(self, pos, model, agent_type):

        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type


    def step(self):
        # Sumatoria del Hamintoniano
        E_s = 0            
        E_f = 0     # Energía si se voltea el spin
        spin = self.type
        spin_f = - spin
        if self.model.normal: 
            # Selecciona si es una distribución normal o uniforme
            u1 = np.random.normal(self.model.media1, self.model.desviacion1)
            u2 = np.random.normal(self.model.media2, self.model.desviacion2)
        else:
            u1 = random.random()
            u2 = random.random()

        for neighbor in self.model.grid.neighbor_iter(self.pos, False): # Alineación Von Neuman
            ng = neighbor.type
            if ng ==1: # si es positivo o cancerosa se una mu_1
                E_s += -spin*ng*u1
                E_f += -spin_f*ng*u1
            else:       # si es -1 SI se una mu_2
                E_s += -spin*ng*u2
                E_f += -spin_f*ng*u2

        E_s = -self.model.J*E_s # Cálculo de las energías
        E_f = -self.model.J*E_f 
        Temp = self.model.T_inv
        r1 = random.random()

        diff_E = E_f - E_s # Diferencia de Energias
        boltzman = np.exp(-diff_E*Temp)
        # Si la energía es menor al hacer el flip entonces se elige ese estado
        if (diff_E <0 and self.model.J !=0):
            spin *= -1
            self.model.total_energy +=diff_E
        elif( r1 < boltzman and self.model.J!=0):
        # Probabilidad que cambie espontaneamente.
            spin *= -1
            self.model.total_energy +=diff_E
        self.type = spin

class Ising(Model):
    """
    Modelo de la clase ISING.
    """

    def __init__(self, height=20, width=20, minority_pc=0.5, T=0.4, J=0.0, normal=False, 
    media1 = 0.5, desviacion1=0.5, media2 = 0.5, desviacion2=0.5):
        """ """
        # atributos del modelo 
        self.height = height
        self.width = width
        self.minority_pc = minority_pc       # El porcentaje de los agentes verdes.
        self.T_inv = 1/T
        self.total_energy =0
        self.J =J
        self.normal=normal
        self.media1 = media1
        self.desviacion1= desviacion1
        self.media2 = media2
        self.desviacion2= desviacion2

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.datacollector = DataCollector(
            {"energy": "energy"}, 
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Inicialización de los agentes
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.minority_pc:
                agent_type = 1              # células cancerosas
            else:
                agent_type = -1             # SI

            agent = IsingAgent((x, y), self, agent_type)
            self.grid.position_agent(agent, (x, y))
            self.schedule.add(agent)
        for cell in self.grid.coord_iter():
            # Energía total
            spin = cell[0].type
            x = cell[1]
            y = cell[2]
            E_s =0
            for neighbor in self.grid.neighbor_iter((x,y), False): # Alineación Von Neuman
                E_s += neighbor.type
            self.total_energy += -E_s*spin/2

        self.running = True
        self.datacollector.collect(self)

    def step(self):

        self.schedule.step()
        # collect data
        self.datacollector.collect(self)




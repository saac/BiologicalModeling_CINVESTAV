# Alberto Josué Ortiz Rosales
# 18 feb 2022

from turtle import width
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Ising


class EnergyElement(TextElement):


    def __init__(self):
        pass

    def render(self, model):
        return "Energy agents: " + str(model.total_energy )


def Ising_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w":1, "h": 1, "Filled": "true", "Layer": 0}

    if agent.type == 1:
        portrayal["Color"] = ["#008000", "#008000"]
        portrayal["stroke_color"] = "#008000"
    else:
        portrayal["Color"] = ["#000000", "#000000"]
        portrayal["stroke_color"] = "#000000"
    return portrayal


energy_element = EnergyElement()
height_canvas = 50
width_canvas =50
canvas_element = CanvasGrid(Ising_draw, height_canvas, width_canvas, 500, 500)
e_chart = ChartModule([{"Label": "total_energy", "Color": "Black"}])

model_params = {
    "height": height_canvas,
    "width": width_canvas,
    "minority_pc": UserSettableParameter("slider", "minority_pc", 0.1, 0.01, 1.0, 0.005),
    "density": UserSettableParameter("slider", "density", 0.1, 0.01, 1.0, 0.005),
    "prob_crecer": UserSettableParameter("slider", "prob_crecer", 0.1, 0.01, 1.0, 0.005),
    "prob_evadir": UserSettableParameter("slider", "prob_evadir", 0.1, 0.01, 1.0, 0.005),


}

server = ModularServer(
    Ising, [canvas_element, energy_element, e_chart], "ISING", model_params
)

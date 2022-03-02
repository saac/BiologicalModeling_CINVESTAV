# Alberto Josué Ortiz Rosales
# 18 feb 2022

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

height = 50
width = 50 
canvas_element = CanvasGrid(Ising_draw, height, width, 500, 500)
e_chart = ChartModule([{"Label": "total_energy", "Color": "Black"}])

model_params = {
    "height": height,
    "width": width,
    "minority_pc": UserSettableParameter("slider", "Porcentaje de verdes", 0.5, 0.01, 1.0, 0.005),
    "T": UserSettableParameter("slider", "T (temperatura)", 0.4, 0.0, 5, 0.1),
    "J": UserSettableParameter("slider", "J", -0.5, -2, 2, 0.01),
    "normal": UserSettableParameter("checkbox", "Distribución normal de mu1 y mu2", value=False),
    "media1": UserSettableParameter("number", "Media mu1", value=0.5),
    "desviacion1": UserSettableParameter("number", "Desviación estandar mu1", value=0.5),
    "media2": UserSettableParameter("number", "Media mu2", value=0.5),
    "desviacion2": UserSettableParameter("number", "Desviación estandar m2", value=0.5),

}


server = ModularServer(
    Ising, [canvas_element, energy_element, e_chart], "ISING", model_params
)

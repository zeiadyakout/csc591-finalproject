import numpy as np
import pandas as pd

def processWine():

    data = pd.read_csv("data/wineQuality/wineQuality.csv")
    x = data[["Fixedacidity", "Volatileacidity", "Citricacid", "Residualsugar", "CL", "FreeSO2", "TotalS02", "Density", "PH", "Sulphates"]]
    y = data[["Alcohol-", "Quality+"]]
    return data, x, y

# the path will be relative to the file but "data/process/pom3a.csv" come to mind as an example. 
# replace a after pom3 with b, c, or d as needed
def processPom(file):
    data = pd.read_csv(file)
    x = data[["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]]
    y = data[["Cost-", "Score-", "Idle-"]]
    return data, x, y



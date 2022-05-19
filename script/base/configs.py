import json
import os
class Configs():
    __configs = None
    __dimension = None
    def __init__(self) -> None:
        pass

    @staticmethod
    def readConfigFile(path):
         with open(path, "r") as file:
            Configs.__configs = json.load(file)

    @staticmethod
    def setDimension(dimension):
        Configs.__dimension = dimension

    @staticmethod
    def getDimension():
        return Configs.__dimension

    @staticmethod
    def getParameter(parameter):
        return Configs.__configs[parameter]

    @staticmethod
    def ufmgMatlabFolder():
        return "~/Documents/MATLAB/bin/"
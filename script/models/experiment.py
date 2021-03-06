from models.log import Log
from models.pattern import Pattern
import itertools
class Experiment():
    def __init__(self, experiment_path, u, dimension) -> None:
        self.__path:str = experiment_path
        # self.__patterns = []
        self.__log = None
        self.__algorithm = None
        self.__u = u
        self.__dimension = dimension
        self.__initialize()

    def __initialize(self):
        algorithm = self.__path.split("/")[-1].split(".")[0]
        self.__algorithm = algorithm

        log_name = f"{algorithm}.log"
        log_path = self.__path.replace(f"/experiments/{algorithm}.experiment", "")
        log_path = f"{log_path}/logs/{log_name}"
        self.__log = Log(log_path)

    def getPatterns(self):
        return (Pattern(pattern, self.__dimension) for pattern in open(self.__path))

    def getFirstNPatterns(self, n):
        return itertools.islice(self.getPatterns(), n)

    def getLog(self):
        return self.__log

    def getU(self):
        return self.__u
    
    def getAlgorithm(self):
        return self.__algorithm

    def getDimension(self):
        return self.__dimension

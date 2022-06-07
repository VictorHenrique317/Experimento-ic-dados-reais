import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time

from post_analysis.plotting_data import PlottingData
from models.attribute import Attribute
from base.configs import Configs
import matplotlib.ticker
from post_analysis.experiment_analysis import ExperimentAnalysis
class Grapher():
    def __init__(self, configuration_name, dataset) -> None:
        # self.__configs = Configs()
        self.__dataset = dataset
        self.__extra_curves = []
        self.__yscale = None
        self.__curves = None
        self.__attribute = None
        self.__ylimits = None
        self.__plotting_data = PlottingData(configuration_name)
        self.__configuration_name = configuration_name
        self.__initialize()

    def __initialize(self):
        algorithms = Configs.getParameter("algorithms")
        truncate_nb = Configs.getParameter("nb_of_truncated_patterns")
        multidupehack = algorithms[0]
        paf = algorithms[1]
        getf = algorithms[2]
        triclusterbox = algorithms[3]
        pafmaxgrow = algorithms[4]
        multidupehack_paf = "Multidupehack + Paf"
        truncated_paf = f"First {truncate_nb} Paf patterns"
        
        self.__curves = {multidupehack:"blue", paf:"red", multidupehack_paf:"purple", \
                 getf:"darkgreen", truncated_paf:"magenta", triclusterbox:"brown", pafmaxgrow:"palevioletred"}

    def setAttribute(self, attribute: Attribute):
        self.__attribute = attribute
        self.__configureGraphForAttribute(attribute)

    def setYLimits(self, y_min, y_max):
        self.__ylimits = [y_min, y_max]

    def __configureGraphForAttribute(self, attribute: Attribute):
        if attribute == Attribute.PATTERN_NUMBER:
            self.__yscale = "log"
        elif attribute == Attribute.MEMORY:
            self.__yscale = "log"
        elif attribute == Attribute.QUALITY:
            self.__yscale = "linear"
            experiment_analysis = ExperimentAnalysis(self.__configuration_name, self.__dataset)
            experiment_analysis.setQualityForExperimentClusters()

        elif attribute == Attribute.TRUNCATED_QUALITY:
            self.__yscale = "linear"
        elif attribute == Attribute.RUN_TIME:
            self.__yscale = "log"
        else:
            print(f"No attribute configuration for {attribute.value}")

    def __configureCurve(self,x,y,curve):
        color = self.__curves[curve]
        plt.scatter(x,y, color=color)
        plt.plot(x,y, color=color, label=curve)
        plt.legend()
        plt.grid()
        plt.title(f"{self.__attribute.value}")
        plt.xlabel("u")
        plt.xlim(max(x), min(x))
        plt.ylabel(self.__attribute.value)
        axis = plt.gca()
        axis.set_ylim(self.__ylimits)
        plt.yscale(self.__yscale)
        # axis.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        # axis.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
        #
        # axis.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        # axis.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

        # axis.set_xticks(list(x))
        axis.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        axis.get_yaxis().set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:.1f}'))

        axis.set_xticks(Configs.getParameter('u_values'))

    def __dataForCombinedRuntime(self,u):
        self.__plotting_data.setAlgorithm("Multidupehack")
        self.__plotting_data.setAttribute(Attribute.RUN_TIME)
        self.__plotting_data.setU(u)
        x1,y1 = self.__plotting_data.getXY()

        self.__plotting_data.setAlgorithm("Paf")
        self.__plotting_data.setAttribute(Attribute.RUN_TIME)
        self.__plotting_data.setU(u)
        x2,y2 = self.__plotting_data.getXY()

        y1 = [number for number in y1]
        y2 = [number for number in y2]
        print(len(y2))
        print(y1)
        print(y2)
        y3 = [y1[i] + y2[i] for i in range(len(y1))] 
        return (x1, y3)

    def __isEmpty(self, x,y):
        return len(x) == 0 and len(y) ==0

    def __drawCurves(self):
        for algorithm in Configs.getParameter("algorithms"):
            self.__plotting_data.setAlgorithm(algorithm)
            self.__plotting_data.setAttribute(self.__attribute)
            x, y = self.__plotting_data.getXY()
            if self.__isEmpty(x,y): # algorithm not runned
                continue
            
            self.__configureCurve(x,y,algorithm)

        for curve in self.__curves:
            truncate_nb = Configs.getParameter("nb_of_truncated_patterns")
            truncated_paf = f"First {truncate_nb} Paf patterns"
            # if self.__attribute == Attribute.RUN_TIME and curve == "Multidupehack + Paf":
            #     x,y = self.__dataForCombinedRuntime(u)
            #     if self.__isEmpty(x,y): # multidupehack or/and paf not runned
            #         continue
            #     self.__configureCurve(x,y,curve, u)

            if self.__attribute == Attribute.QUALITY and curve == truncated_paf:
                self.__plotting_data.setAlgorithm("Paf")
                self.__plotting_data.setAttribute(Attribute.TRUNCATED_QUALITY)
                x,y = self.__plotting_data.getXY()
                if self.__isEmpty(x,y): # paf not runned
                    continue
                self.__configureCurve(x,y,curve)

    def drawGraph(self, folder, save):
        # for u in Configs.getParameter("u_values"):
        fig, ax = plt.subplots()
        fig = plt.figure(figsize=(12, 9))
        self.__drawCurves()

        if save:
            filename = self.__attribute.value.lower().replace(" ", "-")
            filename = f"{filename}.png"
            plt.savefig(f"{folder}/{filename}")
            plt.close(fig)
        else:
            plt.show()

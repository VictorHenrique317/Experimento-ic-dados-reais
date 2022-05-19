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
    def __init__(self, configuration_name) -> None:
        # self.__configs = Configs()
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
        cancer = algorithms[4]
        pafmaxgrow = algorithms[5]
        multidupehack_paf = "Multidupehack + Paf"
        planted_patterns_number = "Number of planted patterns"
        truncated_paf = f"First {truncate_nb} Paf patterns"
        
        self.__curves = {multidupehack:"blue", paf:"red", multidupehack_paf:"purple", \
                 getf:"darkgreen", planted_patterns_number:"orange", truncated_paf:"magenta", triclusterbox:"brown",\
                 cancer:"lime", pafmaxgrow:"palevioletred"}

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
            experiment_analysis = ExperimentAnalysis(self.__configuration_name)
            experiment_analysis.setQualityForExperimentClusters()
            time.sleep(10)  # wait writing qualities to archives

        elif attribute == Attribute.TRUNCATED_QUALITY:
            self.__yscale = "linear"
        elif attribute == Attribute.RUN_TIME:
            self.__yscale = "log"
        else:
            print(f"No attribute configuration for {attribute.value}")

    def __configureCurve(self,x,y,curve,u):
        color = self.__curves[curve]
        plt.scatter(x,y, color=color)
        plt.plot(x,y, color=color, label=curve)
        plt.legend()
        plt.grid()
        plt.title(f"{self.__attribute.value} for u={u}")
        plt.xlabel("Nb. of correct observations")
        plt.xlim(max(x), min(x))
        plt.ylabel(self.__attribute.value)
        axis = plt.gca()
        axis.set_ylim(self.__ylimits)
        plt.xscale("log", basex=2)
        plt.yscale(self.__yscale)
        axis.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        axis.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
        
        axis.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        axis.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

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

    def __drawCurves(self, u):
        for algorithm in Configs.getParameter("algorithms"):
            self.__plotting_data.setAlgorithm(algorithm)
            self.__plotting_data.setAttribute(self.__attribute)
            self.__plotting_data.setU(u)
            x, y = self.__plotting_data.getXY()
            if self.__isEmpty(x,y): # algorithm not runned
                continue
            
            self.__configureCurve(x,y,algorithm, u)

        for curve in self.__curves:
            truncate_nb = Configs.getParameter("nb_of_truncated_patterns")
            truncated_paf = f"First {truncate_nb} Paf patterns"
            # if self.__attribute == Attribute.RUN_TIME and curve == "Multidupehack + Paf":
            #     x,y = self.__dataForCombinedRuntime(u)
            #     if self.__isEmpty(x,y): # multidupehack or/and paf not runned
            #         continue
            #     self.__configureCurve(x,y,curve, u)

            if self.__attribute == Attribute.PATTERN_NUMBER and curve == "Number of planted patterns":
                x = Configs.getParameter("correct_obs")

                pattern_number = Configs.getParameter("n_patterns")
                y = [pattern_number for i in range(len(x))]
                self.__configureCurve(x,y,curve, u)

            if self.__attribute == Attribute.QUALITY and curve == truncated_paf:
                self.__plotting_data.setAlgorithm("Paf")
                self.__plotting_data.setAttribute(Attribute.TRUNCATED_QUALITY)
                self.__plotting_data.setU(u)
                x,y = self.__plotting_data.getXY()
                if self.__isEmpty(x,y): # paf not runned
                    continue
                self.__configureCurve(x,y,curve, u)

    def drawGraph(self, folder, save):
        for u in Configs.getParameter("u_values"):
            fig, ax = plt.subplots()
            self.__drawCurves(u)

            if save:
                filename = self.__attribute.value.lower().replace(" ", "-")
                filename = f"{filename}-for-u-{u}.png"
                plt.savefig(f"{folder}/{filename}")
                plt.close(fig)
            else:
                plt.show()

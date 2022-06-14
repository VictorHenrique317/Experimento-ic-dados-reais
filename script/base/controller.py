from numpy import True_
from base.configs import Configs
from base.numpy_translator import NumpyTranslator
from models.attribute import Attribute
from utils.commands import Commands
from post_analysis.grapher import Grapher
from base.file_system import FileSystem
from multiprocessing import Process
from base.retweets_dataset import RetweetsDataset


class Controller():
    def __init__(self) -> None:
        # self.dataset = RetweetsDataset()
        self.dataset = RetweetsDataset()
        self.__configs_folder = "configs"
        self.dataset_folder = "../datasets"
        self.base_dataset_path = f"{self.dataset_folder}/retweets-sparser-processed"
        self.algorithms = []
        self.__numpy_translator = NumpyTranslator(self)

        self.__current_iteration_number = None
        self.current_configuration_name = None
        self.current_iteration_folder = None
        self.current_dataset = None
        self.current_experiment = None

        Configs.setDimension(len(self.dataset.getDimension()))

    def addAlgorithm(self, algorithm):
        if algorithm not in self.algorithms:
            self.algorithms.append(algorithm)
    
    def __run(self):
        FileSystem.createIterationFolder()

        # Configs.setDimension(self.dataset.getDimension())
        self.__numpy_translator.run(self.dataset)

        for u in Configs.getParameter("u_values"):
            print("="*120 + f" U VALUE = {u}")
            self.current_experiment = f"u{u}"
            FileSystem.createExperimentFolder(self.current_experiment, self.current_configuration_name)

            for algorithm in self.algorithms:
                if algorithm.hasTimedOut(u):
                    continue

                timedout = algorithm.run(u, Configs.getParameter("timeout"))
                if timedout:
                    algorithm.timedOut(u)
                    print("Deleting files...")
                    FileSystem.deleteExperiment(self.current_configuration_name, u, algorithm.name)
                print("-"*120)

    def __resetAlgorithms(self):
        for algorithm in self.algorithms:
            algorithm.resetTimeOutInfo()

    def initiateSession(self):
        FileSystem.deleteIterationFolder()
        FileSystem.deletePostAnalysisFolder()

        for config_file in Commands.listFolder(self.__configs_folder):
            Configs.readConfigFile(f"{self.__configs_folder}/{config_file}")
            self.current_configuration_name = Configs.getParameter("configuration_name")
            self.__resetAlgorithms()
            self.__run()
                    
    def __analyseConfiguration(self, configuration_name, save):
        FileSystem.createPostAnalysisFolder(configuration_name)
        post_analysis_folder = f"../post_analysis/{configuration_name}" 
        grapher = Grapher(configuration_name, self.dataset)
        print("Plotting pattern nb graph")
        grapher.setAttribute(Attribute.PATTERN_NUMBER)
        grapher.setYLimits(0.6, 3_200_000)
        grapher.drawGraph(post_analysis_folder, save)

        print("Plotting memory graph")
        grapher.setAttribute(Attribute.MEMORY)
        grapher.setYLimits(1e-2, 500)
        grapher.drawGraph(post_analysis_folder, save)

        print("Plotting run time graph")
        grapher.setAttribute(Attribute.RUN_TIME)
        grapher.setYLimits(1, 10_000)
        grapher.drawGraph(post_analysis_folder, save)

        print("Plotting quality graph")
        grapher.setAttribute(Attribute.QUALITY)
        grapher.setYLimits(0, 1.1)
        grapher.drawGraph(post_analysis_folder, save)
        grapher.drawGraph(post_analysis_folder, save)

    def initiatePostAnalysis(self, save=True):
        print("#"*120)
        FileSystem.deletePostAnalysisFolder()

        for config_file in Commands.listFolder(self.__configs_folder):
            Configs.readConfigFile(f"{self.__configs_folder}/{config_file}")
            self.current_configuration_name = Configs.getParameter("configuration_name")

            print(f"Initiating post analysis for {self.current_configuration_name}...")
            self.__analyseConfiguration(self.current_configuration_name, save=save)

    def getParameter(self, parameter):
        return Configs.getParameter(parameter)

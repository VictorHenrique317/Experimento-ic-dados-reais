from base.file_system import FileSystem
from post_analysis.quality import Quality
from base.configs import Configs
class ExperimentAnalysis():
    def __init__(self, configuration_name) -> None:
        self.__configuration_name = configuration_name
        # self.__experiment_clusters = []
        # self.__configs = Configs()
        # self.__initialize()

    # def __initialize(self):
    #     self.__experiment_clusters = FileSystem.getExperimentClusters()

    def __setQualityForExperiment(self, experiment):
        planted_patterns = FileSystem.getPlantedPatterns(experiment.getIteration(), self.__configuration_name)
        quality = Quality.calculate(experiment, planted_patterns)
        experiment.getLog().writeAttribute("Quality", quality)

    def __setQualityForTruncatedExperiment(self, experiment):
        number = Configs.getParameter("nb_of_truncated_patterns")
        planted_patterns = FileSystem.getPlantedPatterns(experiment.getIteration(), self.__configuration_name)

        quality = Quality.calculate(experiment, planted_patterns, truncate_number=number)
        experiment.getLog().writeAttribute("Truncated quality", quality)

    def __setQualityForExperimentCluster(self, cluster):
        cluster.loadExperiments()
        for experiment in cluster.getExperiments():
            if experiment.getAlgorithm() == "paf":
                self.__setQualityForTruncatedExperiment(experiment)

            self.__setQualityForExperiment(experiment)

    def setQualityForExperimentClusters(self):
        print(f"Calculating qualities for {self.__configuration_name}...")
        
        experiment_clusters = FileSystem.getExperimentClusters(self.__configuration_name)
        counter = 0
        for cluster in experiment_clusters:
            counter += 1
            self.__setQualityForExperimentCluster(cluster)
            print(f"{100*counter/len(experiment_clusters): .2f}% done")


    
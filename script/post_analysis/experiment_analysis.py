from base.file_system import FileSystem
from post_analysis.quality import Quality
from base.configs import Configs
from utils.quality_normalizer import QualityNormalizer

from models.attribute import Attribute


class ExperimentAnalysis():
    def __init__(self, configuration_name, dataset) -> None:
        self.__configuration_name = configuration_name
        self.__dataset = dataset
        self.__normalizer = None # implementar

    def __setQualityForTruncatedExperiment(self, dataset_matrix, experiment):
        number = Configs.getParameter("nb_of_truncated_patterns")
        quality = Quality.calculate(dataset_matrix, experiment, truncate_number=number)
        experiment.getLog().writeAttribute(Attribute.TRUNCATED_QUALITY.value, quality)

    def __setQualityForExperimentCluster(self, dataset_matrix, cluster):
        # cluster.loadExperiments()
        for experiment in cluster.getExperiments():
            if experiment.getAlgorithm() == "paf":
                self.__setQualityForTruncatedExperiment(dataset_matrix, experiment)

            quality = Quality.calculate(dataset_matrix, experiment)
            experiment.getLog().writeAttribute(Attribute.QUALITY.value, quality)

    def __normalizeQualities(self, dataset_matrix, experiment_clusters):
        print("Normalizing qualities...")

        normalizer = QualityNormalizer(dataset_matrix ,experiment_clusters)
        for cluster in experiment_clusters:
            for experiment in cluster.getExperiments():
                log = experiment.getLog()
                log.writeAttribute(Attribute.QUALITY.value, normalizer.normalize(log.getAttributeValue(Attribute.QUALITY)))

                if experiment.getAlgorithm == "paf":
                    log.writeAttribute(Attribute.TRUNCATED_QUALITY.value, normalizer.normalize(log.getAttributeValue(Attribute.TRUNCATED_QUALITY)))
        print(normalizer.normalize(Quality.getWorstQuality(dataset_matrix)))


    def setQualityForExperimentClusters(self):
        print(f"Calculating qualities for {self.__configuration_name}...")
        dataset_matrix = self.__dataset.toMatrix()
        experiment_clusters = FileSystem.getExperimentClusters(self.__configuration_name)
        counter = 0
        for cluster in experiment_clusters:
            counter += 1
            self.__setQualityForExperimentCluster(dataset_matrix, cluster)
            print(f"{100*counter/len(experiment_clusters): .2f}% done")

        self.__normalizeQualities(dataset_matrix, experiment_clusters)


    
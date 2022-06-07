from algorithm.algorithm import Algorithm
from base.controller import Controller
import time
from utils.commands import Commands
class TriClusterBox(Algorithm):
    def __init__(self, controller:Controller) -> None:
        super().__init__()
        self.name = "triclusterbox"
        self.__controller = controller
        self.__controller.addAlgorithm(self)

    def __writeLog(self, elapsed_time):
        nb_patterns = None
        with open(self.experiment_path) as file:
            nb_patterns = sum([1 for line in file])

        with open(self.log_path, "a") as file:
            file.write(f"Run time: {elapsed_time}\n")
            file.write(f"Nb of patterns: {nb_patterns}")

    def run(self, u, observations, timeout):
        current_experiment = self.__controller.current_experiment
        configuration_name = self.__controller.current_configuration_name

        self.experiment_path = f"../iteration/{configuration_name}/output/{current_experiment}/experiments/triclusterbox.experiment"
        self.log_path = f"../iteration/{configuration_name}/output/{current_experiment}/logs/triclusterbox.log"
        fuzzy_tensor_path = f"../iteration/{configuration_name}/tensors/numnoise/dataset-co{observations}.fuzzy_tensor"
        multidupehack_path = f"../iteration/{configuration_name}/output/{current_experiment}/experiments/multidupehack.experiment"

        command = f"/usr/bin/time -o {self.log_path} -f 'Memory (kb): %M' "
        command += f"pp -f{fuzzy_tensor_path} {multidupehack_path} "
        command += f"-o {self.log_path}"
        
        print(command)
        start = time.time()
        timedout = Commands.executeWithTimeout(command, timeout)      
        end = time.time()
        elapsed_time = end - start

        if timedout is False:
            self.__writeLog(elapsed_time)

        return timedout
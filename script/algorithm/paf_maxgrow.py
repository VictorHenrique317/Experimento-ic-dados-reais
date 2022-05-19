from algorithm.algorithm import Algorithm
from base.controller import Controller
from utils.commands import Commands
class PafMaxGrow(Algorithm):
    def __init__(self, controller:Controller) -> None:
        super().__init__()
        self.name = "pafmaxgrow"
        self.__controller = controller
        self.__controller.addAlgorithm(self)

    def run(self, u, observations, timeout):
        current_experiment = self.__controller.current_experiment
        current_iteration_folder = self.__controller.current_iteration_folder

        self.experiment_path = f"{current_iteration_folder}/output/{current_experiment}/experiments/pafmaxgrow.experiment"
        self.log_path = f"{current_iteration_folder}/output/{current_experiment}/logs/pafmaxgrow.log"
        multidupehack_path = f"{current_iteration_folder}/output/{current_experiment}/experiments/multidupehack.experiment"
        fuzzy_tensor_path = f"{current_iteration_folder}/tensors/numnoise/dataset-co{observations}.fuzzy_tensor"

        if Commands.fileExists(multidupehack_path) is False:
            print("WARNING: Multidupehack file does not exist, skipping paf...")
            return True

        command = f"/usr/bin/time -o {self.log_path} -f 'Memory (kb): %M' "
        command += f"cat {fuzzy_tensor_path} | "
        command += f"paf -o {self.experiment_path} -f "
        command += f"- -a0 {multidupehack_path} "
        command += f">> {self.log_path}"
        print(command)
        return Commands.executeWithTimeout(command, timeout)

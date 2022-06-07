from algorithm.algorithm import Algorithm
from base.controller import Controller
from utils.commands import Commands
class Paf(Algorithm):
    def __init__(self, controller:Controller) -> None:
        super().__init__()
        self.name = "paf"
        self.__controller = controller
        self.__controller.addAlgorithm(self)

    def run(self, u, timeout):
        a = self.__controller.getParameter("a")

        current_experiment = self.__controller.current_experiment
        configuration_name = self.__controller.current_configuration_name

        self.experiment_path = f"../iteration/{configuration_name}/output/{current_experiment}/experiments/paf.experiment"
        self.log_path = f"../iteration/{configuration_name}/output/{current_experiment}/logs/paf.log"
        multidupehack_path = f"../iteration/{configuration_name}/output/{current_experiment}/experiments/multidupehack.experiment"
        translated_tensor_path = f"{self.__controller.base_dataset_path}.txt"

        if Commands.fileExists(multidupehack_path) is False:
            print("WARNING: Multidupehack file does not exist, skipping paf...")
            return True

        command = f"/usr/bin/time -o {self.log_path} -f 'Memory (kb): %M' "
        command += f"cat {translated_tensor_path} | "
        command += f"paf -o {self.experiment_path} -f "
        command += f"- -a{a} {multidupehack_path} "
        command += f">> {self.log_path}"
        print(command)
        return Commands.executeWithTimeout(command, timeout)


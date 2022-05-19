from algorithm.algorithm import Algorithm
from base.controller import Controller
from utils.commands import Commands
class Multidupehack(Algorithm):
    def __init__(self, controller:Controller) -> None:
        super().__init__()
        self.name = "multidupehack"
        self.__controller = controller
        self.__controller.addAlgorithm(self)

    def __calculateEpsilon(self, u): 
        size = self.__controller.getParameter("s")
        dimension = self.__controller.getParameter("dataset_size")
        dimension = len(dimension) - 1
        return float(f"{size**dimension*(1-u): .1f}")

    def run(self, u, observations, timeout):
        dataset_size = self.__controller.getParameter("dataset_size")
        dimension = len(dataset_size)

        s = self.__controller.getParameter("s")
        s = " ".join([str(s) for i in range(dimension)]).strip()

        e = self.__calculateEpsilon(u)
        e = " ".join([str(e) for i in range(dimension)]).strip()

        current_experiment = self.__controller.current_experiment
        current_iteration_folder = self.__controller.current_iteration_folder

        self.experiment_path = f"{current_iteration_folder}/output/{current_experiment}/experiments/multidupehack.experiment"
        self.log_path = f"{current_iteration_folder}/output/{current_experiment}/logs/multidupehack.log"
        fuzzy_tensor_path = f"{current_iteration_folder}/tensors/numnoise/dataset-co{observations}.fuzzy_tensor"

        command = f"/usr/bin/time -o {self.log_path} -f 'Memory (kb): %M' "
        command += f"multidupehack -s'{s}' "
        command += f"-e '{e}' {fuzzy_tensor_path} "
        command += f"-o {self.experiment_path} "
        command += f">> {self.log_path}"
        
        print(command)
        return Commands.executeWithTimeout(command, timeout)           

from algorithm.algorithm import Algorithm
from base.controller import Controller
from utils.commands import Commands
class Multidupehack(Algorithm):
    def __init__(self, controller:Controller) -> None:
        super().__init__()
        self.name = "multidupehack"
        self.__controller = controller
        self.__controller.addAlgorithm(self)

    def __calculateEpsilons(self, u):
        s = self.__controller.getParameter("s")
        e = []
        for i in range(3):
            ei = (1-u)

            for j, sj in enumerate(s):
                if j == i:
                    continue
                ei *= sj

            e.append(ei)

        return e

    def run(self, u, timeout):
        s = self.__controller.getParameter("s")
        s = " ".join([str(i) for i in s]).strip()

        e = self.__calculateEpsilons(u)
        e = " ".join([str(i) for i in e]).strip()

        current_experiment = self.__controller.current_experiment
        configuration_name = self.__controller.current_configuration_name

        self.experiment_path = f"../iteration/{configuration_name}/output/{current_experiment}/experiments/multidupehack.experiment"
        self.log_path = f"../iteration/{configuration_name}/output/{current_experiment}/logs/multidupehack.log"
        translated_tensor_path = f"{self.__controller.base_dataset_path}.txt"

        command = f"/usr/bin/time -o {self.log_path} -f 'Memory (kb): %M' "
        command += f"multidupehack -s'{s}' "
        command += f"-e '{e}' {translated_tensor_path} "
        command += f"-o {self.experiment_path} "
        command += f">> {self.log_path}"
        
        print(command)
        return Commands.executeWithTimeout(command, timeout)           

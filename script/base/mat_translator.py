import numpy as np
from scipy.io import savemat
class MatTranslator():
    def __init__(self, controller) -> None:
        self.__controller = controller

    def __toNumpy(self, dataset):
        dataset_path = dataset.path()
        translated_tensor = np.zeros(dataset.getDimension())
        # depth, row, column
        
        with open(dataset_path) as file:
            for line in file:
                line = [float(character) for character in line.split(" ")]
                value = line[-1] 
                dims = [int(dim) for dim in line[:-1]]

                replacer_string = f"translated_tensor{dims} = {value}"
                exec(replacer_string)

        return translated_tensor

    def run(self, dataset):
        numpy_tensor = self.__toNumpy(dataset)
        numpy_tensor = {"matrix": numpy_tensor, "label": "matrix"}

        mat_path = f"{self.__controller.dataset_folder}/retweets-sparser-processed.mat"
        savemat(mat_path, numpy_tensor)
        print("Translated fuzzy tensor to mat matrix")
        print("-"*120)
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder

class RetweetsDataset():
    def __init__(self):
        self.__path = "../datasets/retweets-sparser"
        self.__preprocess()

    def path(self):
        return self.__path

    def getDimension(self):
        columns = dict()
        with open(self.__path) as database:
            for line in database:
                line = line.strip().split(" ")

                for column in range(len(line)):
                    value = line[column]
                    column_set = columns.get(column, set())
                    column_set.add(value)

                    columns[column] = column_set

        columns = {column: len(column_set) for column, column_set in columns.items()}
        return [size for size in columns.values()][:-1]

    def toMatrix(self):
        dataset = pd.read_csv(self.__path, sep=' ', header=None)
        dataset = dataset.iloc[:, :].values
        matrix = np.zeros(self.getDimension())

        nb_indices = dataset.shape[0]
        for line in range(nb_indices):
            index = [int(dimension) for dimension in dataset[:, :-1][line]]
            density = dataset[:, -1][line]
            replacer_string = f"matrix{index} = {density}"
            exec(replacer_string)

        return matrix

    def __preprocess(self):
        print("Pre-processing dataset...")

        dataset = pd.read_csv(self.__path, sep=' ', header=None)
        dataset = dataset.iloc[:, :].values
        le = LabelEncoder()
        dataset[:, 0] = le.fit_transform(dataset[:, 0])
        dataset[:, 1] = le.fit_transform(dataset[:, 1])
        dataset[:, 2] = le.fit_transform(dataset[:, 2])
        dataset = pd.DataFrame(data=dataset)

        self.__path = "../datasets/retweets-sparser-processed.txt"
        dataset.to_csv(self.__path, header=False, sep=" ", index=False)

        print("Dataset was pre-processed!")


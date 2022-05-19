from base.controller import Controller
from algorithm.multidupehack import Multidupehack
from algorithm.paf import Paf
from algorithm.getf import Getf
from base.file_system import FileSystem
from post_analysis.plotting_data import PlottingData
from models.attribute import Attribute
from models.log import Log
from post_analysis.experiment_analysis import ExperimentAnalysis
from models.pattern import Pattern
from post_analysis.quality import Quality
from base.mat_translator import MatTranslator
from base.retweets_dataset import RetweetsDataset

import time
from itertools import count
from multiprocessing import Process

database = RetweetsDataset("../datasets/retweets-sparser")
database.preprocess()



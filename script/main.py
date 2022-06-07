from base.controller import Controller
from algorithm.multidupehack import Multidupehack
from algorithm.triclusterbox import TriClusterBox
from algorithm.paf import Paf
from algorithm.paf_maxgrow import PafMaxGrow
from algorithm.getf import Getf
from base.file_system import FileSystem

from utils.commands import Commands

controller = Controller()
multidupehack = Multidupehack(controller)
paf = Paf(controller)
pafmaxgrow = PafMaxGrow(controller)
getf = Getf(controller)
# triclusterbox = TriClusterBox(controller)

# controller.initiateSession()
controller.initiatePostAnalysis()


import re
from base.configs import Configs
from models.attribute import Attribute
class Log():
    def __init__(self, path):
            self.path = path
            self.__attributes = None
            self.__algorithm = None
            # self.__configs = Configs()
            self.__initialize()

    def getAttributes(self):
        return self.__attributes
    
    def getAlgorithm(self):
        return self.__algorithm

    def __initialize(self):
        self.__setAlgorithmFromPath()

        data = dict() # {attribute: value}
        with open(self.path) as log:
            
            for line in log:
                match = re.findall("(.*):(.*)", line)
                if len(match) == 0 or len(line) == 0:
                    continue
                
                translated_attribute = self.__translateAttribute(match[0][0])
                if translated_attribute is None: # attribute not relevant
                    continue

                value = self.__translateValue(translated_attribute, match[0][1])
                # print(translated_attribute, value)
                data[translated_attribute] = value
        self.__attributes = data

    def __setAlgorithmFromPath(self):
        algorithm = self.path.split("/")[-1]
        algorithm = algorithm.split(".")[0]
        self.__algorithm = algorithm

    def __translateAttribute(self, attribute): # translates different names for same attribute 
        attributes_dict = Configs.getParameter("plot_attributes")
        for translated_attribute, variants in attributes_dict.items():

            if self.__algorithm == "multidupehack":
                if variants[0] in attribute or variants[2] in attribute or variants[3] in attribute:
                    return translated_attribute

            if self.__algorithm == "paf":
                if attribute == variants[1]:
                    return translated_attribute

            if self.__algorithm == "getf":
                if attribute == variants[1]:
                    return translated_attribute     

            if self.__algorithm == "triclusterbox":
                if attribute == variants[1]:
                    return translated_attribute 

            if self.__algorithm == "cancer":
                if attribute == variants[1]:
                    return translated_attribute     
            
            if self.__algorithm == "pafmaxgrow":
                if attribute == variants[1]:
                    return translated_attribute

            if attribute == translated_attribute: # generic case
                return translated_attribute

    def __translateValue(self, attribute, value):
        value = value.strip()
        value = re.findall("(\d*\.*\d*)", value)[0]
        value = float(value)
        if attribute == "Memory (mb)":
            value /= 1000

        return value

    def __deleteLastTwoLines(self):
        lines = None
        with open(self.path, 'r') as log:
            lines = [line for line in log]
            del lines[-1]
            del lines[-2]

        with open(self.path, 'w+') as new_log:
            for line in lines:
                new_log.write(line)

    def writeAttribute(self, attribute, value):
        if attribute in self.__attributes: # delete last two lines
            self.__deleteLastTwoLines()

        with open(self.path, "a") as file:
            line = f"\n{attribute}:{value}\n"
            file.write(line)
        self.__initialize()

    def getAttributeValue(self, attribute:Attribute):
        return self.__attributes.get(attribute.value, 0)
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
                if variants[0] in attribute or variants[2] in attribute:
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
        value = float(re.findall("(\d*\.*\d*)", value)[0])
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


class AveragedLog():
    def __init__(self, algorithm, averaged_attributes) -> None:
        self.__averaged_attributes = averaged_attributes
        self.__algorithm = algorithm

    def getAttributeValue(self, attribute:Attribute):
        return self.__averaged_attributes.get(attribute.value, 0)

    def getAttributes(self):
        return self.__averaged_attributes

    def getAlgorithm(self):
        return self.__algorithm

    @staticmethod
    def average(log_groups): # twin logs from different iterations [[m_log, p_log], [m_log, p_log]]
        averaged_algorithm_attributes = dict() # {algorithm: {attr1:value1, attr2:value2}}
        for log_group in log_groups:
            for log in log_group:
                algorithm = log.getAlgorithm()
                averaged_attributes = averaged_algorithm_attributes.setdefault(algorithm, dict())

                attributes = log.getAttributes()
                for attribute, value in attributes.items():
                    averaged_value = averaged_attributes.setdefault(attribute, 0)
                    averaged_value += value
                    averaged_attributes[attribute] = averaged_value

        nb_iterations = len(log_groups)
        averaged_logs = []
        for algorithm, attributes in averaged_algorithm_attributes.items():
            for attribute, value in attributes.items():
                attributes[attribute] = value/nb_iterations
            
            averaged_log = AveragedLog(algorithm, attributes)
            averaged_logs.append(averaged_log)
        
        return averaged_logs
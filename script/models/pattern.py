class Pattern():
    def __init__(self, pattern, dimension) -> None:
        self.__dimension = dimension
        self.__pattern = self.__formatPattern(pattern)

    def __formatPattern(self, pattern):
        if type(pattern) == list: # already formated
            return pattern
        
        pattern = pattern.replace("\n", "").strip()
        if len(pattern) == 0: # empty pattern
            return [set() for i in range(self.__dimension)]

        pattern =  pattern.split(" ")
        if len(pattern) > self.__dimension:
            del pattern[-1] # deletes the density of the pattern found by paf
            
        return [set(numbers.split(",")) for numbers in pattern]

    def area(self):
        pattern_area = 1
        for ith_tuple in self.__pattern:
            pattern_area *= len(ith_tuple)
        return pattern_area

    def intersection(self, pattern): # returns a pattern that is the intersection of both
        intersection = []
        pattern = pattern.get()
        for i in range(self.__dimension):
            ith_tuple1 = self.__pattern[i] # {'1', '2'}
            ith_tuple2 = pattern[i] # {'1', '3'}
            intersection.append(ith_tuple1.intersection(ith_tuple2))
        return Pattern(intersection, self.__dimension)

    def union(self, pattern):
        union = []
        pattern = pattern.get()        
        
        for i in range(self.__dimension):
            ith_tuple1 = self.__pattern[i] # {'1', '2'}
            ith_tuple2 = pattern[i] # {'1', '3'}
            union.append(ith_tuple1.union(ith_tuple2))
        return Pattern(union, self.__dimension)

    def intersectionArea(self, pattern):
        return self.intersection(pattern).area()

    def unionArea(self, pattern):
        return self.union(pattern).area()

    def jaccardIndex(self, pattern):
        intersection = self.intersectionArea(pattern)
        union = self.unionArea(pattern)
        return intersection / union # 0 <= return <= 1

    def get(self):
        return self.__pattern

    def getDimension(self):
        return self.__dimension
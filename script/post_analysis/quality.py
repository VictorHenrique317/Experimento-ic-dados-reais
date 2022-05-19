from base.file_system import FileSystem
from models.pattern import Pattern
from base.configs import Configs
import itertools

class Quality():

    @staticmethod
    def __findMostSimilarFoundPattern(planted_pattern, found_patterns):
        # returns the most similar found pattern to a given planted one
        most_similar_pattern = None
        higher_jaccard = -1

        for found_pattern in found_patterns:
            jaccard_index = found_pattern.jaccardIndex(planted_pattern)
            if jaccard_index >= higher_jaccard:
                higher_jaccard = jaccard_index
                most_similar_pattern = found_pattern
        return most_similar_pattern

    @staticmethod
    def __multiplePatternUnion(patterns):
        dimension = len(Configs.getParameter("dataset_size"))
        union = Pattern("", dimension)
        for pattern in patterns:
            union = union.union(pattern)
        return union

    @staticmethod
    def __multiplePatternUnionArea(patterns):
        return Quality.__multiplePatternUnion(patterns).area()

    @staticmethod
    def calculate(experiment, planted_patterns, truncate_number=None):
        try:
            empty_test = experiment.getPatterns()
            next(empty_test)
        except StopIteration: # no patterns found by the algorithm
            return 0 # zero quality

        all_p_intersection_argmax = []
        for planted_pattern in planted_patterns:
            if truncate_number is None:
                most_similar_found = Quality.__findMostSimilarFoundPattern(planted_pattern, experiment.getPatterns())
            else:
                found_patterns = (pattern for index, pattern in enumerate(experiment.getPatterns()) if index < truncate_number)
                most_similar_found = Quality.__findMostSimilarFoundPattern(planted_pattern, found_patterns)

            p_intersection_argmax = most_similar_found.intersection(planted_pattern)
            all_p_intersection_argmax.append(p_intersection_argmax)

        numerator = Quality.__multiplePatternUnionArea(all_p_intersection_argmax)

        planted_patterns_union = Quality.__multiplePatternUnion(planted_patterns)

        if truncate_number is None:
            found_patterns_union = Quality.__multiplePatternUnion(experiment.getPatterns())
        else:
            found_patterns = (pattern for index, pattern in enumerate(experiment.getPatterns()) if index < truncate_number)
            found_patterns_union = Quality.__multiplePatternUnion(found_patterns)

        denominator = planted_patterns_union.unionArea(found_patterns_union)
        return numerator / denominator
        

        


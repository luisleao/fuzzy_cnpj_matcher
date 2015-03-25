import time
from fuzzyset import FuzzySet

__author__ = 'paulo.rodenas'


class SequentialFuzzyCnpjMatcher:

    def __init__(self):
        self.__cnpj_bases = []

        for x in xrange(0, 100):
            idx = x * 1000000
            self.__cnpj_bases.append('../bulk/cnpjs_base_' + str(idx).zfill(7) +
                                     '.txt')

        self.__fuzzy_matcher = None

    def match_cnpj(self, cnpj, debug=False):
        best_matches = []

        for cnpj_base_str in self.__cnpj_bases:
            with open(cnpj_base_str) as f:
                # temp variables
                start_time = time.time()

                # Searching
                self.__log('Searching for %s on %s' % (cnpj, cnpj_base_str), debug)
                self.__fuzzy_matcher = FuzzySet(f.read().splitlines())

                match = self.__fuzzy_matcher.get(cnpj)
                elapsed_time = time.time() - start_time

                self.__log('Best match for this file is %s and it took %d seconds'
                           % (match, elapsed_time), debug)
                # Appending to the best matches so far
                if not match is None:
                    for m in match:
                        best_matches.append(m[1])

        # Performing Fuzzy string match on the best results of each cnpj base file
        self.__fuzzy_matcher = FuzzySet(best_matches)
        return self.__fuzzy_matcher.get(cnpj)[0]

    def __log(self, msg, debug=False):
        if debug:
            print msg
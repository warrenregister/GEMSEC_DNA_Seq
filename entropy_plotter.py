'''
Class for performing entropy analysis upon datasets and plotting
the results.
'''

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from operator import add
from translation import translate
import entropy_plotting as ep


class entropy_plotter():
    def __init__(self, datasets):
        '''
        Initiates entropy_plotter with a list of datasets in self.sets and
        empty dictionaries for each set within both self.data and 
        self.total_entropy

        datasets: a list of all sets to be analyzed
        '''
        self.sets = datasets
        self.data = {}
        self.total_entropy = {}
        for setnum, dataset in enumerate(self.data):
            self.total_entropy['Set' + str(setnum + 1)] = {}
            self.data['Set' + str(setnum + 1)] = {}
    

    def split_sets(self):
        '''
        Splits each dataset in self.sets into the filtered combinations of
        each's washes needed for entropy analysis. Populated self.data dict
        witch each combination of washes per each set.
        '''

        for setnum, dataset in enumerate(self.sets):
            wash_combs = ep.split_set(dataset)
            comb_names = self.name_wash_combs(wash_combs)
            for index, wash in enumerate(wash_combs):
                self.data['Set' + str(setnum + 1)][comb_names[index]] = wash


    def name_wash_combs(self, wash_combs):
        '''
        Returns a list of representative names for a list of the different
        filtered combinations of washes for a set's washes.

        wash_combs: list of filtered combinations of a set's washes
        '''
        curname = 'w'
        names = []
        for washnum, wash in enumerate(wash_combs):
            if washnum < len(wash_combs) - 1:
                curname += str(washnum)
            else:
                curname += 'e'
            names.append(curname)

        return names
    

    def calc_entropy(self):
        '''
        Calculates entropy for each wash combination within each set and puts
        the values in self.total_entropy. 
        '''

        for dataset in self.data.keys():
            for wash_comb in self.data[dataset].keys():
                self.total_entropy[dataset][wash_comb] = ep.calc_entropy(ep.generate_matrices(self.data[dataset][wash_comb]))
    

    def plots(self):
        ep.plot1(total_entropy, 'test_plot1')
        ep.plot2(total_entropy, 'test_plot2')
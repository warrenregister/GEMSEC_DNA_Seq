import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from operator import add
from translation import translate
from operator import add


class EntropyPlotter():
    '''
    Class for performing entropy analysis upon datasets and plotting
    the results.
    '''
    def __init__(self, datasets:list):
        '''
        Initiates entropy_plotter with a list of datasets in self._sets and
        empty dictionaries for each set within both self._data and 
        self._total_entropy

        datasets: a list of all sets to be analyzed
        '''
        self._sets = datasets
        self._data = {} # Dict for each wash combination to later plot
        self._total_entropy = {} # Dict for entropy value per wash combination
        for setnum, dataset in enumerate(self._sets):
            self._total_entropy['Set' + str(setnum + 1)] = {}
            self._data['Set' + str(setnum + 1)] = {}
    

    def split_sets(self):
        '''
        Splits each dataset in self._sets into the filtered combinations of
        each's washes needed for entropy analysis. Populated self._data dict
        witch each combination of washes per each set.
        '''
        for setnum, dataset in enumerate(self._sets):
            sampling_tuple = self.split_set(dataset)
            wash_combs = self.sample_datasets(sampling_tuple[0], sampling_tuple[1])
            comb_names = self.name_wash_combs(wash_combs)
            for index, wash in enumerate(wash_combs):
                self._data['Set' + str(setnum + 1)][comb_names[index]] = wash


    @staticmethod
    def name_wash_combs( wash_combs:list):
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
        the values in self._total_entropy. 
        '''

        for dataset in self._data.keys():
            for wash_comb in self._data[dataset].keys():
                self._total_entropy[dataset][wash_comb] = self._entropy_function(
                        self.generate_matrices(
                        self._data[dataset][wash_comb])).sum()/12
    

    def plots(self):
        self.plot1(self._total_entropy, 'test_plot1')
        self.plot2(self._total_entropy, 'test_plot2')
    

    @staticmethod
    def split_set( a_set:pd.DataFrame, sampled:bool = False):
        '''
        Takes in a dataframe representing a single set of an experiment and
        returns a list of filtered datasets, if sampled = True they are 
        sampled so that they are all the same size.
        
        Datasets are filtered so only peptides present in wash 1 are kept,
        then those only in both wash 1 and 2, on until we only see peptides
        which were present in all washes and the eluate. Finally, peptides only present
        in eluate are added as the last dataset.

        a_set: A dataframe containing all washes and the eluate from a set
        sampled: a boolean which determines whether to use random samples from 
        each dataset so that they are all the same size.
        '''
        washes = []
        index = 0
        columns = a_set.columns[1:]
        while 'eluate' != columns[index]:
            washes.append(columns[index])
            index += 1
        washes.append('eluate')
        start_point = a_set.loc[a_set[washes[0]] > 0]
        filtered_datasets = [start_point]
        min_size = len(a_set)

        for index, _ in enumerate(washes):
            filtered_datasets[index] = filtered_datasets[index].loc[
                filtered_datasets[index][washes[index]] > 0]
            filtered_datasets.append(filtered_datasets[index])
            for wash in washes[index + 1:]: 
                filtered_datasets[index] = filtered_datasets[index].loc[
                    filtered_datasets[index][wash] == 0]
            size = len(filtered_datasets[index].index)
            if size < min_size:
                min_size = size

        only_in_eluate = a_set.loc[a_set[washes[0]] == 0]
        for wash in washes[:-1]: 
            only_in_eluate = only_in_eluate.loc[only_in_eluate[wash] == 0]
        filtered_datasets[-1] = (only_in_eluate.loc[a_set['eluate'] > 0])

        return (filtered_datasets, min_size)
    

    @staticmethod
    def sample_datasets(filtered_datasets:list, n:int):
        '''
        Randomly samples datasets so that an equal number of samples are taken
        from each for analysis and graphing. Returns new datasets of equal size.

        filtered_datasets: a list of filtered datasets
        n: size of the smalles dataset in filtered_datasets
        '''

        sampled_filtered_datasets = []
        for index, dataset in enumerate(filtered_datasets):
            sampled_filtered_datasets.append(dataset.sample(n, replace = True))
        return sampled_filtered_datasets
    


    @staticmethod
    def one_hotter(seq:str):
        '''
        One hot encodes a DNA or Peptide sequence.
        Returns a 12x20 matrix which encodes the amino acid at each 
        location in a peptide sequence.
        seq: A sequence of 36 nucleotides or 12 amino acids to encode
        '''
        if len(seq) > 12:
            seq = translate(seq)
        if '_' not in seq:
            aa = "RHKDESTNQCGPAVILMFYW"
            c2i = dict((c,i) for i,c in enumerate(aa))
            int_encoded = [c2i[char] for char in seq]
            onehot_encoded = list()
            for value in int_encoded:
                letter = [0 for _ in range(20)]
                letter[value] = 1
                onehot_encoded.append(letter)
            return(np.matrix(onehot_encoded))
        return 0


    def generate_matrices(self, data:pd.DataFrame):
        '''
        Returns a 12x20 matrix which represents the distribution of amino 
        acids across a database of peptides.
        data: Dataframe of peptides and their counts in a number of 
        washes of a large group of peptides bonded to a substrate
        '''
        sum = np.zeros((12,20), dtype=np.float64)
        data['mult'] = data[data.columns[1:-1]].sum(axis=1) / len(data)
        seqs = data.sequence
        data.drop('sequence', axis=1, inplace = True)
        for count, seq in enumerate(seqs): 
            onehot_encoded = self.one_hotter(seq)
            sum += onehot_encoded * data['mult'].iloc[count]
        return(np.matrix(sum))


    @staticmethod
    def entropy_function(matrix:np.matrix):
        '''
        Calculates the shannon entropy for a matrix representing the
        distribution of amino acids across a dataset of peptide
        sequences. Returns the information entropy for the given matrix.

        matrix: a 12x20 matrix representing the distributions of the 20
        amino acids across a dataset of 12 amino acid length peptides.
        '''
        row_sum = matrix.sum()
        pr = matrix / row_sum 
        entropy_func_val = np.multiply(pr, np.log(pr))
        entropy_func_val = np.nan_to_num(entropy_func_val)
        entropy_func_val = entropy_func_val.sum(axis=1, dtype='float') * -1
        return entropy_func_val


    def plot1(self, ent:dict, title:str):
        '''
        Plots a bar graph for each set for entropy across washes

        ent: Dictionary containing Information Entropy within each 
        wash of each set.
        title: name to save graph under
        '''
        for set_name in self._data:
            vals = list(ent[set_name].values())
            x = np.arange(len(vals))
            plt.bar(x, vals)
            plt.title('Entropy across washes - ' + set_name)
            plt.ylabel('Information Entropy')
            plt.xticks(x, list(self._data[set_name].keys()))
            plt.savefig(f'./pep_'+set_name+'_'+title)
            plt.show()


    def plot2(self, ent:dict, title:str):
        '''
        Averages entropy across sets and plots across washes

        ent: Dictionary containing Information Entropy within each 
        wash of each set.
        title: name to save graph under
        '''
        setsEnt = list(ent['Set1'].values())
        for set_name in list(self._data.keys())[1:]:
            setsEnt = list(map(add, setsEnt, list(ent[set_name].values())))
        setsEnt = [i/len(setsEnt) for i in setsEnt]
        x = np.arange(len(setsEnt))
        vals = setsEnt
        plt.bar(x, vals)
        plt.title('Entropy across washes - all sets')
        plt.ylabel('Information Entropy')
        plt.xticks(x, ('W1', 'W12', 'W123', 'W123E', 'E'))
        plt.savefig(f'./'+title)
        plt.show()   
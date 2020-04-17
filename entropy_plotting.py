'''
Contains methods for calculating and plotting the entropy of a set 
of NGS etexperimental data.
'''
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from operator import add
from translation import translate



def split_set(a_set:pd.DataFrame, sampled:bool = False):
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
    washes = list(a_set.columns[1:])
    washes.append('eluate')
    start_point = a_set.loc[a_set[washes[0]] > 0]
    filtered_datasets = [start_point]
    min_size = len(a_set)

    for index, _ in enumerate(washes):
        filtered_datasets[index] = filtered_datasets[index].loc[filtered_datasets[index][washes[index]] > 0]
        filtered_datasets.append(filtered_datasets[index])
        for wash in washes[index + 1:]: 
            filtered_datasets[index] = filtered_datasets[index].loc[filtered_datasets[index][wash] == 0]
        size = len(filtered_datasets[index].index)
        if size < min_size:
            min_size = size

    only_in_eluate = a_set.loc[a_set[washes[0]] == 0]
    for wash in washes[:-1]: 
        only_in_eluate = only_in_eluate.loc[only_in_eluate[wash] == 0]
    filtered_datasets[-1] = (only_in_eluate.loc[a_set['eluate'] > 0])

    return(sample_datasets(filtered_datasets, min_size))


def sample_datasets(filtered_datasets, n):
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


def generate_matrices(data:pd.DataFrame):
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
        onehot_encoded = one_hotter(seq)
        sum += onehot_encoded * data['mult'][count]
    return(np.matrix(sum))


def calc_entropy(matrix):
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


def plot1(ent, title):
    '''
    Plots a bar graph for each set for entropy across washes

    ent: Dictionary containing Information Entropy within each 
    wash of each set.
    title: name to save graph under
    '''
    x = np.arange(5)
    for i in ['Set1','Set2','Set3']:
        vals = list(ent[i].values())
        plt.bar(x, vals)
        plt.title('Entropy across washes - ' + i)
        plt.ylabel('Information Entropy')
        plt.xticks(x, ('W1', 'W12', 'W123', 'W123E', 'E'))
        plt.savefig(f'./pep_'+i+'_'+title)
        plt.show()


def plot2(ent, title):
    '''
    Averages entropy across sets and plots across washes

    ent: Dictionary containing Information Entropy within each 
    wash of each set.
    title: name to save graph under
    '''
    setsEnt = list(map(add, list(ent['Set1'].values()), 
                       list(ent['Set2'].values())))
    setsEnt = list(map(add, setsEnt, list(ent['Set3'].values())))
    setsEnt = [i/3 for i in setsEnt]
    x = np.arange(5)
    vals = setsEnt
    plt.bar(x, vals)
    plt.title('Entropy across washes - all sets')
    plt.ylabel('Information Entropy')
    plt.xticks(x, ('W1', 'W12', 'W123', 'W123E', 'E'))
    plt.savefig(f'./'+title)
    plt.show()   
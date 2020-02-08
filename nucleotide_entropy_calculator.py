import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

class nucleotide_entropy_calculator():
    def __init__(self):
        self.total = np.zeros((36,4))
        aa = "ATCG"
        self.c2i = dict((c,i) for i,c in enumerate(aa))
        

    def add_sequence(self, seq, total):
        int_encoded = [self.c2i[char] for char in seq]
        onehot_encoded = list()
        for value in int_encoded:
            letter = [0 for _ in range(4)]
            letter[value] = 1
            onehot_encoded.append(letter)
        
        self.total += np.matrix(onehot_encoded) * total


    def computes_entropy(self):
        total_acgt = self.total[0].sum()
        avgs = self.total / total_acgt
        entropy_func_val = np.multiply(avgs, np.log(avgs))
        entropy_func_val = entropy_func_val.sum(axis=1, dtype='float') * -1
        self.info_entropy = np.sum(entropy_func_val)/36
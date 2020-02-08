import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from translation import translate

class amino_acid_entropy_calculator():
    def __init__(self):
        self.entropies = pd.DataFrame() 
        self.total = np.zeros((12,21))
        aa = "IMTNKSRLPHQVADEGFYCW"
        self.c2i = dict((c,i) for i,c in enumerate(aa))
        

    def add_sequence(self, seq, total):
        acids = translate(seq)
        int_encoded = [self.c2i[char] for char in acids]
        onehot_encoded = list()
        for value in int_encoded:
            letter = [0 for _ in range(21)]
            letter[value] = 1
            onehot_encoded.append(letter)
        
        self.total += np.matrix(onehot_encoded) * total


    def computes_entropy(self):
        total_acgt = self.total[0].sum()
        avgs = self.total / total_acgt
        entropy_func_val = np.multiply(avgs, np.log(avgs))
        self.entropy_func_val = entropy_func_val.sum(axis=1, dtype='float') * -1 # column wise sum
        self.info_entropy = np.sum(entropy_func_val)/12 # row wise sum

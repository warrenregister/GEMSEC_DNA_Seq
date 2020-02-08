import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

# per wash, per location, distribution of total counts - distribution per wash, 

class entropy_plotter():
    def __init__(self, entropies_list):
        self.entropies = pd.DataFrame()
        for info_entropy in entropies_list:
            self.entropies.append([info_entropy])
    

    def plotter(self):
        sets = ['set_1','set_2','set_3']
        y_pos = np.arange(len(sets))
        plt.bar(sets, list(self.entropies[0]))
        plt.xticks(y_pos, sets)
        plt.savefig(f'./Plots/all_DNA_entropy.png')
        plt.close() 
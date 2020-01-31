# Author: Nitya Krishna Kumar

import numpy as np
import matplotlib.pyplot as plt

#-- Accounting for Total Population -------------------------------------------------------------

# One Hot Encodes a DNA Sequence
def DNA1hotter(seq):
    aa = "ATCG"
    c2i = dict((c,i) for i,c in enumerate(aa))
    int_encoded = [c2i[char] for char in seq]
    onehot_encoded = list()
    for value in int_encoded:
        letter = [0 for _ in range(len(aa))]
        letter[value] = 1
        onehot_encoded.append(letter)
    return(onehot_encoded)


entropies = pd.DataFrame() # will contain entropies for set 1, 2, 3
for i in ['set_1','set_2','set_3']:
    data_all = pd.read_csv('./ngs1_mos2_' + i + 'all_DNA_counts.csv')
    sequences = data_all.Seq
    total = np.zeros((36,4))
    for index, seq in enumerate(sequences):
        seq_list = list(seq)
        
        # deletes sequences with non A, C, G, T values
        if not seq_list.__contains__('N'):
            one_hot = DNA1hotter(seq)
            val = data_all.Total[index]
            one_hot = np.matrix(one_hot)
            encoded_with_counts = one_hot * val
            total = total + one_hot
    
    # computes info-entropy: sum(-sum())
    total_acgt = total[0].sum()
    avgs = total/total_acgt
    entropy_func_val = np.multiply(avgs, np.log(avgs))
    entropy_func_val = entropy_func_val.sum(axis=1, dtype='float') * -1
    info_entropy = np.sum(entropy_func_val)/36
    entropies = entropies.append([info_entropy])

# plot entropies
sets = ['set_1','set_2','set_3']
y_pos = np.arange(len(sets))

plt.bar(sets, list(entropies[0]))
plt.xticks(y_pos, sets)
plt.savefig(f'./Plots/all_DNA_entropy.png')
plt.close()
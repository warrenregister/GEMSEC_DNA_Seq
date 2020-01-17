import pandas as pd 

class nucleotide_counter():

    def __init__(self, file_name):
        columns = ['G', 'T', 'C', 'A']
        index = range(36)
        self.nucleotides = pd.DataFrame(columns=columns, index=index)
        self.nucleotides.fillna(0)
        self.name = file_name
        for num in range(36):
            self.nucleotides.append([0,0,0,0])
    
    def add_barcode(self, barcode):
        for position, nucleotide in enumerate(barcode):
            self.nucleotides[nucleotide][position] += 1
    
    def write_csv(self):
        self.nucleotides.to_csv(self.name + '_nuc_counts.csv')

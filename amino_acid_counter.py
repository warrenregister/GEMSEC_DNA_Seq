import pandas as pd 
from translation import translate

class amino_acid_counter():
    def __init__(self, file_name):
        self.name = file_name
        index = range(12)
        acids = ['I','M','T','N','K','S','R','L','P','H','Q','V','A','D','E','G','F','Y','C','_','W']
        self.amino_acids = pd.DataFrame(columns=acids, index=index)
        self.amino_acids.fillna(0)
        self.amino_acids.columns = acids
        for num in range(len(acids)):
            self.amino_acids.append(pd.Series(0, index=self.amino_acids.columns), ignore_index=True)
    
    def add_barcode(self, seq):
        peptide = translate(seq)
        for position, acid in enumerate(peptide):
            self.amino_acids[acid][position] += 1
    
    def write_csv(self):
        self.amino_acids.to_csv(self.name + '_amino_acid_counts.csv')
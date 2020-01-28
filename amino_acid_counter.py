import pandas as pd 
from translation import translate

class amino_acid_counter():
    def __init__(self, file_name):
        self.name = file_name
        index = range(12)
        acids = ['I','M','T','N','K','S','R','L','P','H','Q','V','A','D','E','G','F','Y','C','_','W']
        self.amino_acids = pd.DataFrame(columns=acids, index=index)
        for col in self.amino_acids:
            for row in range(36):
                self.amino_acids[col][row] = 0
        self.amino_acids.columns = acids
    
    def add_barcode(self, seq):
        peptide = translate(seq)
        for position, acid in enumerate(peptide):
            self.amino_acids[acid][position] += 1
    
    def write_csv(self):
        name_chunks = self.name.split('_')
        self.amino_acids.to_csv('./FASTQfiles/fakeFASTQ/aminoCounts/' + name_chunks[1] + name_chunks[2] + '_amino_acid_counts.csv')
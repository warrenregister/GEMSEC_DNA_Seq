import pandas as pd 

class nucleotide_counter():

    def __init__(self, file_name):
        columns = ['G', 'T', 'C', 'A']
        index = range(36)
        self.nucleotides = pd.DataFrame(columns=columns, index=index)
        for col in self.nucleotides:
            for row in range(36):
                self.nucleotides[col][row] = 0
        self.name = file_name.split('/')[-1]
    
    def add_barcode(self, barcode):
        for position, nucleotide in enumerate(barcode):
            if nucleotide != '\n':
                self.nucleotides[nucleotide][position] += 1
    
    def write_csv(self):
        self.nucleotides.to_csv('./FASTQfiles/fakeFASTQ/nucCounts/' + self.name.split('.')[0] + '_nuc_counts.csv')

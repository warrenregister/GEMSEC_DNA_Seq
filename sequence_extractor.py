#!/usr/bin/env python
import os
import pandas as pd
import easygui as eg
from nucleotide_counter import nucleotide_counter
from amino_acid_counter import amino_acid_counter
import itertools


# Class for taking DNA sequences out of FASTQ format and converting to a csv 
# with counts for each unique sequence.
class sequence_extractor():
    # fileName: name of a csv file, path included
    # Initiate blank dicitionary, check that given file exists and is FASTQ
    def __init__(self, fileName):  
        self.fileName = fileName
        self.seqs = {}
        if not os.path.exists(fileName):  # Check if given file is real
            raise SystemError("Error: File does not exist\n")
        fastqFormats = ['fq', 'FASTQ', 'fastq']  # Check if a file is the proper format
        if self.fileName.split('.')[-1] not in fastqFormats:
            raise SystemError("Error: File does not have FASTQ file extension\n")
    
    # Extract each DNA sequence from FASTQ file, add each to dictionary
    # with the values being a count of each's occurrences
    def extract(self):
        with open(self.fileName) as fastq:  # Open file, store contents as fastq
            self.nuc_counter = nucleotide_counter(self.fileName)
            self.amino_counter = amino_acid_counter(self.fileName)
            for line in itertools.islice(fastq, 1, None, 4): # Gets only the DNA sequences from the fastq file (start = 1, stop = None, step = 4)
                if line not in self.seqs:
                    self.seqs[line] = 1
                else:
                    self.seqs[line] += 1
                self.nuc_counter.add_barcode(line)
                self.amino_counter.add_barcode(line)
                
                
    def write_CSV(self):  # Write dictionary of DNA sequences to a csv file
        if not os.path.exists("./FASTQfiles/fakeFASTQ/nucCounts"):
            os.mkdir('./FASTQfiles/fakeFASTQ/nucCounts')
        if not os.path.exists('./FASTQfiles/fakeFASTQ/aminoCounts'):
            os.mkdir('./FASTQfiles/fakeFASTQ/aminoCounts')
            
        CSV = pd.DataFrame.from_dict(self.seqs, orient='index')
        CSV.to_csv('./'+self.fileName.split('.')[1]+'.csv')
        self.nuc_counter.write_csv()
        self.amino_counter.write_csv()


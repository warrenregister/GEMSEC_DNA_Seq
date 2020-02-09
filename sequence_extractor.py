#!/usr/bin/env python
import os
import pandas as pd
import easygui as eg
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
            for line in itertools.islice(fastq, 1, None, 4): # Gets only the DNA sequences from the fastq file (start = 1, stop = None, step = 4)
                if line not in self.seqs:
                    self.seqs[line] = 1
                else:
                    self.seqs[line] += 1
        return(pd.DataFrame.from_dict(self.seqs, orient='index'))
                
    def write_CSV(self, path):  # Write dictionary of DNA sequences to a csv file
        
        print("CSV path: "+path+self.fileName.split('/')[-1].split('.')[0]+'.csv')
        CSV = pd.DataFrame.from_dict(self.seqs, orient='index')
        CSV.to_csv(path+self.fileName.split('/')[-1].split('.')[0]+'.csv')


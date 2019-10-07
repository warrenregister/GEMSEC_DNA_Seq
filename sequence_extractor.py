#!/usr/bin/env python
import os
import pandas as pd
import easygui as eg


# Class for taking 36 char DNA sequences out of FASTQ format and converting to a csv 
# with counts for each unique sequence.
class sequence_extractor():
    # Initiate blank dicitionary, check that given file exists and is FASTQ
    def __init__(self, fileName):  
        self.fileName = fileName
        self.seqs = {}
        if not os.path.exists(fileName):  # Check if given file is real
            raise SystemError("Error: File does not exist\n")
        fastqFormats = ['fq', 'FASTQ', 'fastq']  # Check if a file is the proper format
        if self.fileName.split('.')[1] not in fastqFormats:
            raise SystemError("Error: File does not have FASTQ file extension\n")
    
    # Extract each 36 char DNA sequence from FASTQ file, add each to dictionary
    #  with the values being a count of each's occurrences
    def extract(self):
        with open(self.fileName) as fastq:  # Open file, store contents as fastq
            lines = []
            for line in fastq:
                lines.append(line.rstrip())  # Add line to list, remove trailing spaces
                if len(lines) == 4:  # Every 4 lines, add a DNA sequence to dictionary
                    if lines[1] not in self.seqs:
                        self.seqs[lines[1]] = 1
                    else:
                        self.seqs[lines[1]] += 1
                    lines = []


    def write_CSV(self):  # Write dictionary of DNA sequences to a csv file
        CSV = pd.DataFrame.from_dict(self.seqs, orient='index')
        CSV.to_csv(self.fileName.split('.')[0]+'.csv')


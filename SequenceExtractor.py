import os
import pandas as pd
import easygui as eg
import itertools



class SequenceExtractor():
    '''
    Class for extracting DNA sequences from FASTQ files and storing them in
    a more compact CSV file which instead of having entries per each instance
    of a sequence, has an extra column which counts the number of times a 
    sequence occurs in a FASTQ file.
    '''
    def __init__(self, files):  
        '''
        Initiate blank dicitionary to be filled with converted FASTQ files,
        check that given file exists and is FASTQ 
        files: path to a FASTQ file or list / dictionary of FASTQ files
        '''
        self._fileNames = list(files)
        self._seqs = {}
        for fileName in self._fileNames:
            if not os.path.exists(fileName):  # Check if given file is real
                raise SystemError("Error: File does not exist\n")
            fastqFormats = ['fq', 'FASTQ', 'fastq']  # Check if a file is the proper format
            if fileName.split('.')[-1] not in fastqFormats:
                raise SystemError("Error: File does not have FASTQ file extension\n")
    
    

    def extract(self):
        '''
        Extract each DNA sequence from FASTQ file, add each to dictionary
        with the values being a count of each's occurrences
        '''
        for fileName in self._fileNames:
            with open(fileName) as fastq:  # Open file, store contents as fastq
                for line in itertools.islice(fastq, 1, None, 4): # Gets only the DNA sequences from the fastq file (start = 1, stop = None, step = 4)
                    if line not in self._seqs:
                        self._seqs[line] = 1
                    else:
                        self._seqs[line] += 1
        return(pd.DataFrame.from_dict(self._seqs, orient='index'))
     
                
    def write_CSV(self, path:str):  
        '''
        Write dictionary of DNA sequences to a csv file
        '''
        for fileName in self._fileNames:
            print("CSV path: "+path+fileName.split('/')[-1].split('.')[0]+'.csv')
            CSV = pd.DataFrame.from_dict(self._seqs, orient='index')
            CSV.to_csv(path+fileName.split('/')[-1].split('.')[0]+'.csv')
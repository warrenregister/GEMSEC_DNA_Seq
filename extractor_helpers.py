from sequence_extractor import SequenceExtractor
import os
import pandas as pd


def extract_csvs(directory:str):
    '''
    Takes in a directory containing FASTQ files with Peptide DNA sequences
    within, extracts the DNA sequences and counts their occurrences in
    each file into a CSV file, returns a dictionary with a list of CSVs for
    each experimental set contained in the directory.
    '''
    csvs = {}
    set_dict = get_wash_versions(directory)
    for set_num in set_dict.keys():
        if set_num != 'csvs':
            csvs[set_num] = []
            for wash_num in set_dict[set_num].keys():
                extractor = SequenceExtractor(set_dict[set_num][wash_num])
                csvs[set_num].append(extractor.extract())
                print("Files extracted...")
    return csvs


def get_wash_versions(directory:str):
    '''
    Returns a dictionary of dictionaries of each version (a, b, etc.) of each
    wash in each set of experiments contained in the given directory. 
    Dictionary labels are set name -> wash name -> wash version file path. 
    If the directory contains csv files, adds those to returned dictionary in
    a list under 'csvs' key.
    '''
    versions = {}
    versions['csvs'] = []
    for fileName in os.listdir(directory):
        names = fileName.split('_') # file name : set#_wash#_irrelevant.fastq
        if names[-1 ][-5:] in ['FASTQ', 'fastq']: # check if fastq file
            if names[0] not in versions: # check if set is in versions dict
                versions[names[0]] = {}
            if names[1] not in versions[names[0]]: # check if wash in set dict
                versions[names[0]][names[1]] = []
            versions[names[0]][names[1]].append(directory + '/' + fileName)
        elif names[-1] == 'csv': # checks if csv, add to versions if so
            versions['csvs'].append(directory + '/' + fileName) 
    return versions
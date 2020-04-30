import os
import sys
import time
import pandas as pd
from EntropyPlotter import EntropyPlotter
from extractor_helpers import extract_csvs
from SequenceMerger import SequenceMerger


def main():
    directory = '/Users/warren/Desktop/docs/GEMSEC_DNA_Seq/FASTQfiles/realFASTQ'
    #directory = sys.argv[1] # uses the given directory (1st command line arg) to look at the FASTQ file

    dfs = extract_csvs(directory) # Dict of each set's extracted FASTQ files
    
    sets = []
    for set_num in dfs.keys():
        merger = SequenceMerger(directory , dfs[set_num])
        sets.append(merger.merge_data())

    entropy_calculator = EntropyPlotter(sets)
    entropy_calculator.split_sets()
    entropy_calculator.calc_entropy()
    entropy_calculator.plots()


if __name__ == '__main__':
    main()

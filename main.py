import os
import sys
import time
import pandas as pd
from entropy_plotter import entropy_plotter
from sequence_extractor import sequence_extractor
from sequence_csv_merger import sequence_csv_merger



# Prompt user for whether they want to convert 1 FASTQ file, convert a folder of FASTQ files,
# or merge a folder of CSVs (previously converted from FASTQ) into 1 CSV
def main():
    directory = '/Users/warren/Desktop/docs/GEMSEC_DNA_Seq/FASTQfiles/realFASTQ'
    #directory = sys.argv[1] # uses the given directory (1st command line arg) to look at the FASTQ file

    csvs = []
    for fileName in os.listdir(directory):
        if fileName.split('.')[-1] in ['fq', 'FASTQ', 'fastq']:
            extractor = sequence_extractor(directory + '/' + fileName)
            csvs.append(extractor.extract())
            print("Files extracted...")
        elif fileName.split('.')[-1] == 'csv':
            csvs.append(pd.read_csv(directory + '/' + fileName))
    
    merger = sequence_csv_merger(directory , csvs)
    merged_file = merger.merge_data()

    entropy_calculator = entropy_plotter(merged_file)
    entropy_calculator.split_sets()
    entropy_calculator.calc_entropy()
    entropy_calculator.plots()


if __name__ == '__main__':
    main()

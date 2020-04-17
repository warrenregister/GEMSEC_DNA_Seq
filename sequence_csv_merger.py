import pandas as pd 


# Class for merging a folder full of CSVs converted from FASTQ files into 1 CSV with columns
# for each CSVs DNA sequence occurence count, and 1 more column for total occurence counts.
class sequence_csv_merger():
    # path: a path to a directory with CSV files to merge into one CSV
    # Initiate sequence_csv_merger w/ empty csv_sizes list
    def __init__(self, path, files):
        self.files = files
        self.path = path
        self.csv_names = [('wash' + str(num)) for num, _ in enumerate(files)]
        self.csv_names[-1] = 'eluate'

    # Merge DataFrames together into 1 DataFrame with DNA sequences as index, create 
    # separate columns per counts of each DataFrame, create a column for total 
    # counts across all DataFrames for each sequence.
    def merge_data(self, wash_num = 1):
        merged_dict = pd.concat(self.files, axis=1, sort=False).fillna(value=0)
        merged_dict.columns = [x for x in self.csv_names]
        merged_dict['total_occurences'] = merged_dict.sum(axis=1) 
        merged_dict.reset_index(inplace=True)
        merged_dict.rename(columns={'index':'sequence', '0':'index'}, inplace=True)
        self.df = merged_dict
        return(merged_dict)


    # name: optional parameter to give merged CSV a specific name
    # Convert dictionary to DataFrame and write it to a CSV file
    def write_CSV(self, name='totals'):
        self.df.to_csv(self.path + name + '.csv')


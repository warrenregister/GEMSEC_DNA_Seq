import pandas as pd 
import glob
import csv


# Class for merging a folder full of CSVs converted from FASTQ files into 1 CSV with columns
# for each CSVs DNA sequence occurence count, and 1 more column for total occurence counts.
class sequence_csv_merger():
    # path: a path to a directory with CSV files to merge into one CSV
    # Initiate sequence_csv_merger w/ empty csv_sizes list
    def __init__(self, path):
        self.path = path
        self.csv_names = []

    def get_data(self):  # Get all csvs in file, convert to DataFrames, put in list
        all_csvs = glob.glob(self.path + '*.csv')  # List of all files in directory ending in .csv
        df_from_each_file = []  # list to contain each csv when it is converted to a DataFrame
        for csv in all_csvs:
            df=pd.read_csv(csv)
            df.columns=['DNA_seq', 'counts']
            df.set_index('DNA_seq', inplace=True)
            df_from_each_file.append(df)
            self.csv_names.append(csv.split('.')[1])  # Get name of CSV
        self.dfs = df_from_each_file

    # Merge DataFrames together into 1 DataFrame with DNA sequences as index, create 
    # separate columns per counts of each DataFrame, create a column for total 
    # counts across all DataFrames for each sequence.
    def merge_data(self): 
        merged_dict = pd.concat(self.dfs, axis=1, sort=False).fillna(value=0)
        merged_dict.columns = [x for x in self.csv_names]
        set_name = self.csv_names[0].split('_')[0]
        merged_dict[set_name] = merged_dict.sum(axis=1) 
        self.dict = merged_dict


    # name: optional parameter to give merged CSV a specific name
    # Convert dictionary to DataFrame and write it to a CSV file
    def write_CSV(self, name='totals'):
        self.dict.to_csv(self.path + name + '.csv')


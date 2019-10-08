import pandas as pd 
import glob


# Class for merging a folder full of CSVs converted from FASTQ files into 1 CSV with columns
# for each CSVs DNA sequence occurence count, and 1 more column for total occurence counts.
class sequence_csv_merger():
    # path: a path to a directory with CSV files to merge into one CSV
    # Initiate sequence_csv_merger w/ empty csv_sizes and csv_names lists
    def __init__(self, path):
        self.path = path
        self.csv_sizes = []
        self.csv_names = []
    
    def merge(self):  # Merge all CSVs in path into one DataFrame.
        all_csvs = glob.glob(self.path + '*.csv')  # List of all files in directory ending in .csv
        df_from_each_file = []  # list to contain each csv when it is converted to a DataFrame
        for csv in all_csvs:
            df_from_each_file.append(pd.read_csv(csv))
            self.csv_sizes.append(sum(1 for row in open(csv)))  # Get number of entries in CSV
            self.csv_names.append(csv.split(self.path)[1].split('.')[0])  # Get name of CSV
        self.concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)


    # Convert merged DataFrame to Dictionary, create a list to keep track of DNA sequence occurence
    # numbers for each CSV, and add extra column for total occurences of each sequence in all CSVs.
    def sort_merged_csv(self):  
        columns = list(self.concatenated_df)
        merged_dict = {}
        count = 1  # count of row of current CSV
        index = 0  # index of csv_sizes to keep track of which CSV is currently being worked on
        cols = len(self.csv_sizes) + 1  # num of cols represented in lists stored in merged dict
        for sequence in self.concatenated_df[columns[0]]:
            # if count = the current CSVs size, move on to the next set, reset count
            if (self.csv_sizes[index] - count) <= 0: 
                    index += 1
                    count = 1
            if sequence not in merged_dict:
                merged_dict[sequence] = [0] * (cols)  # 1 col per CSV, 1 for total

            merged_dict[sequence][index] += 1  # add 1 to col with current part of set
            merged_dict[sequence][cols - 1] += 1  # add 1 to total set occurence count
            count += 1
            

        self.dict = merged_dict


    # name: optional parameter to give merged CSV a specific name
    # Convert dictionary to DataFrame and write it to a CSV file
    def write_CSV(self, name='totals'):
        cols = self.csv_names
        cols.append('Total')
        CSV = pd.DataFrame.from_dict(self.dict, orient='index', columns = cols)
        CSV.to_csv(self.path + '/' + name + '.csv')

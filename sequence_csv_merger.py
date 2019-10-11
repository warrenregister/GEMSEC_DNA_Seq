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
        for count, csv in enumerate(all_csvs):
            df_from_each_file.append(pd.read_csv(csv))
            self.csv_sizes.append(df_from_each_file[count].shape[0])  # Get number of entries in CSV
            self.csv_names.append(csv.split(self.path)[1].split('.')[0])  # Get name of CSV
        self.concatenated_df = df_from_each_file

    # Convert merged DataFrame to Dictionary, create a list to keep track of DNA sequence occurence
    # numbers for each CSV, and add extra column for total occurences of each sequence in all CSVs.
    def sort_merged_csv(self): 
        merged_dict = {}
        cols = len(self.csv_sizes) + 1  # num of cols represented in lists stored in merged dict
        for index, batch in enumerate(self.concatenated_df):
            for count in range(self.csv_sizes[index]):
                if batch['Unnamed: 0'][count] not in merged_dict:
                    merged_dict[batch['Unnamed: 0'][count]] = [0] * (cols)  # 1 col per CSV, 1 for total
                merged_dict[batch['Unnamed: 0'][count]][index] += batch['0'][count] 
                merged_dict[batch['Unnamed: 0'][count]][cols - 1] += batch['0'][count] 
                print('sequence: ' + str(count)+' ' + batch['Unnamed: 0'][count] + ": " + str(batch['0'][count])) 
                

        self.dict = merged_dict


    # name: optional parameter to give merged CSV a specific name
    # Convert dictionary to DataFrame and write it to a CSV file
    def write_CSV(self, name='totals'):
        cols = self.csv_names
        cols.append('Total')
        CSV = pd.DataFrame.from_dict(self.dict, orient='index', columns = cols)
        CSV.to_csv(self.path + '/' + name + '.csv')

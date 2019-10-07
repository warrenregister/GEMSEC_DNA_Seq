import pandas as pd 
import glob

class sequence_csv_merger():
    def __init__(self, path):
        self.path = path
        self.csv_sizes = []
        self.csv_names = []
    
    def merge(self):
        all_csvs = glob.glob(self.path + '*.csv')
        df_from_each_file = []
        for csv in all_csvs:
            df_from_each_file.append(pd.read_csv(csv))
            row_count = sum(1 for row in open(csv))
            self.csv_names.append(csv.split(self.path)[1].split('.')[0])
            self.csv_sizes.append(row_count)
        self.concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

    def sort_merged_csv(self):
        columns = list(self.concatenated_df)
        merged_dict = {}
        count = 1
        index = 0
        for sequence in self.concatenated_df[columns[0]]:
            if (self.csv_sizes[index] - count) <= 0: # if count = current sets size, move to next set
                    index += 1
                    count = 1
            if sequence not in merged_dict:
                merged_dict[sequence] = [0] * (len(self.csv_sizes) + 1) # somehow must grow or shring based on number of csvs...

            merged_dict[sequence][index] += 1 # add 1 to col with current part of set
            merged_dict[sequence][5] += 1  # add 1 to total in set count
            count += 1
            

        self.dict = merged_dict

    def write_CSV(self, name='totals'):
        cols = self.csv_names
        cols.append('Total')
        CSV = pd.DataFrame.from_dict(self.dict, orient='index', columns = cols)
        CSV.to_csv(self.path + '/' + name + '.csv')

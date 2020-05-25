import pandas as pd 


class SequenceMerger():
    '''
    Class for merging a folder full of CSVs converted from FASTQ files into 1 CSV
    with columns for each CSVs DNA sequence occurence count, and 1 more column for
    total occurence counts.
    '''
    def __init__(self, path:str, files:list, totals):
        '''
        Initiate sequence_csv_merger w/ empty csv_sizes list
        path: a path to a directory in which to save the merged file
        files: a list of dataframes or a list of file paths to csv files
        containing DNA sequence data to merge together.
        '''
        self._files = files
        self._path = path
        self._csv_names = [('wash' + str(num)) for num, _ in enumerate(files)]
        self._csv_names[-1] = 'eluate'
        self.totals=totals



    def merge_data(self):
        '''
        Merge DataFrames together into 1 DataFrame with DNA sequences as index
        create separate columns per counts of each DataFrame, create a column 
        for total counts across all DataFrames for each sequence.
        '''
        merged_df = pd.concat(self._files, axis=1, sort=False).fillna(value=0)
        merged_df.columns = [x for x in self._csv_names]
        if self.totals:
            merged_df['total_occurences'] = merged_df.sum(axis=1) 
        merged_df.reset_index(inplace=True)
        merged_df.rename(columns={'index':'sequence', '0':'index'}, inplace=True)
        self._df = merged_df
        return(merged_df)


    def write_CSV(self, name='totals'):
        '''
        Convert dictionary to DataFrame and write it to a CSV file
        name: optional parameter to give merged CSV a specific name
        '''
        self._df.to_csv(self._path + name + '.csv')
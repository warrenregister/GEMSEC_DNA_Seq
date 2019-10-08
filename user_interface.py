import easygui as eg
import os
from sequence_extractor import sequence_extractor
from sequence_csv_merger import sequence_csv_merger


# Class for creating a user interface to simplify the process of converting FASTQ files to CSV files
# and merging multiple CSVs into 1 file.
class user_interface():
    def __init__(self):  # Initiate user_interface, get user choice on action to perform
        choices = ['Open File', 'Open Folder', 'Merge CSVs in Folder']
        msg = 'Do you want to convert 1 file, a set of files, or merge a set of pre-existing CSVs?'
        self.reply = eg.indexbox(msg, choices=choices)
    
    def convert_single_file(self):  # Convert a user-chosen FASTQ file to CSV
        fileName = eg.fileopenbox(default = '*.fq')
        extractor = sequence_extractor(fileName)
        extractor.extract()
        extractor.write_CSV()
        self.success_alert()
    
    # Convert all FASTQ files in a user-chosen directory to CSV, create a CSV with combined
    #  data from all CSVs
    def convert_directory(self):
        directory = eg.diropenbox()
        for fileName in os.listdir(directory):
            if fileName.split('.')[1] in ['fq', 'FASTQ', 'fastq']:
                extractor = sequence_extractor(directory + '/' + fileName)
                extractor.extract()
                extractor.write_CSV()
        self.merge_directory(directory)
    
    # directory: Optional parameter to specifiy directory of CSVs to merge, by defualt calls 
    # easyGUI diropenbox() to get a directory.
    # Merges all csv files in a directory into 1 CSV, preserving all data from combined CSVs.
    def merge_directory(self, directory=None):
        if directory == None:
            directory=eg.diropenbox()
        merger = sequence_csv_merger(directory + '/')
        merger.merge()
        merger.sort_merged_csv()
        merger.write_CSV() 
        self.success_alert()
    

    def success_alert(self):
        if self.reply == 0:
            msg = 'File succesfully converted!'
        elif self.reply == 1:
            msg = 'Files succesfully converted and merged!'
        else:
            msg = 'Files succesfully merged!'
        eg.msgbox(msg=msg, title='Success')

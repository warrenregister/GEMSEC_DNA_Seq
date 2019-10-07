import easygui as eg
import os
from sequenceExtractor import sequence_extractor
from sequence_csv_merger import sequence_csv_merger

class user_interface():
    def __init__(self):
        choices = ['Open File', 'Open Folder']
        msg = 'Do you want to convert 1 file or a set?'
        self.reply = eg.indexbox(msg, choices=choices)
    
    def convert_single_file(self):
        fileName = eg.fileopenbox(default = '*.fq')
        extractor = sequence_extractor(fileName)
        extractor.extract()
        extractor.write_CSV()
    
    def convert_directory(self):
        directory = eg.diropenbox()
        for fileName in os.listdir(directory):
            if fileName.split('.')[1] in ['fq', 'FASTQ', 'fastq']:
                extractor = sequence_extractor(directory + '/' + fileName)
                extractor.extract()
                extractor.write_CSV()
        merger = sequence_csv_merger(directory + '/')
        merger.merge()
        merger.sort_merged_csv()
        merger.write_CSV()    

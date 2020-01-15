import os
from sequence_extractor import sequence_extractor
from sequence_csv_merger import sequence_csv_merger

# Prompt user for whether they want to convert 1 FASTQ file, convert a folder of FASTQ files,
# or merge a folder of CSVs (previously converted from FASTQ) into 1 CSV
def main():
    directory = '/Users/warren/Desktop/docs/GEMSEC_DNA_Seq/FASTQ_files/realFASTQ'
    for fileName in os.listdir(directory):
            if fileName.split('.')[-1] in ['fq', 'FASTQ', 'fastq']:
                extractor = sequence_extractor(directory + '/' + fileName)
                extractor.extract()
                extractor.write_CSV()
    
    merger = sequence_csv_merger(directory + '/')
    merger.get_data()
    merger.merge_data()
    merger.write_CSV()


main()

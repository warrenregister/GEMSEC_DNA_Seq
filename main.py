import os
import sys
import time
from sequence_extractor import sequence_extractor
from sequence_csv_merger import sequence_csv_merger

# Prompt user for whether they want to convert 1 FASTQ file, convert a folder of FASTQ files,
# or merge a folder of CSVs (previously converted from FASTQ) into 1 CSV
def main():
    directory = sys.argv[1] # uses the given directory (1st command line arg) to look at the FASTQ files
    totals_name = sys.argv[2] # name of file that the initial csv totals file will have
    if not os.path.isdir(directory+'/CSV'):
        os.mkdir(directory+'/CSV')
    else:
        if os.path.exists(directory+'/CSV/'+totals_name+'.csv'):
            os.remove(directory+'/CSV/'+totals_name+'.csv')
    print("Extracting files from " + directory + " directory...")
    for fileName in os.listdir(directory):
        if fileName.split('.')[-1] in ['fq', 'FASTQ', 'fastq']:
            extractor = sequence_extractor(directory + '/' + fileName)
            extractor.extract()
            print("Files extracted, converting files to CSV format...")
            extractor.write_CSV(directory + '/CSV/')
    
    merger = sequence_csv_merger(directory + '/CSV/')
    merger.get_data()
    merger.merge_data()
    merger.write_CSV(name = totals_name)

    while not os.path.exists(directory+'/CSV/'+totals_name+'.csv'):
        time.sleep(1)
    
    
    

main()

# GEMSEC_DNA_Seq

### This repo contains a pipeline which takes NGS data and converts and analyses it

The code in this repo's purpose is to create meaningful analysis from NGS (Next Generation Sequencing) data. It will help to predict possible pepetides which will fulfill a specfic purpose such as binding to a specific substrate. It will accomplish by calculating the entropy of each of ~527 distinct properties of amino acids over the possible slots for those properties in the 12 amino acid peptides being sequenced. It will use this entropy data to predict the function of peptides which fall on the entropy datas trend line. 

NGS data takes the form of FASTQ files. This repo contains code which takes these files and perfoms a number of conversion and analysis actions to them, it currently:
+ Converts the FASTQ to csv
+ Counts the number of occurences of each DNA barcode in each file
+ Creates new files to represent the makeup of each set of NGS data inputed


TODO:
+ Store frequency of each type of nucleotide in CSV file formate (36 lines denoting each position, 4 columns denoting frequencies of each type of nucleotide A, T, G, C.
+ Total number of each type of nucleotide (ATGC) at each position in the barcodes (36 nucleotide dna segments)
+ Calculate frequency of each nucleotide in each position in each wash and set for an experiment
+ Total number of each type of amino acid at each slot in the peptides being studied (12 peptide slots)
+ Calculate frequency of each amino acid in each position in each wash and set for an experiment\
+ 


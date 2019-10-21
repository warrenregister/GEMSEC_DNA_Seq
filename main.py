from user_interface import user_interface

# Prompt user for whether they want to convert 1 FASTQ file, convert a folder of FASTQ files,
# or merge a folder of CSVs (previously converted from FASTQ) into 1 CSV
def main():
    gui = user_interface()
    while gui.cont:
        if gui.reply == 0:  # User chose to convert 1 file
            gui.convert_single_file()
        elif gui.reply == 1:  # User chose to convert a folder of files
            gui.convert_directory()
        else:  # User chose to merge a set of files
            gui.merge_directory()


main()

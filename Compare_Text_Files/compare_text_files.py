#! python3
"""
Project:    Utilities
Filename:   compare_text_files
Created by: PJC
Created on: August 25, 2016
"""

import argparse
import difflib
import logging
import os

# Gather arguments which contain paths and file names for the files to be used.
args = argparse.ArgumentParser(prog='file_compare.py',
                               description='This script will compare the contents of two files, the differences found'
                                           ' will be logged to a file.  Both files to be compared are required'
                                           ' arguments.  The differences will be placed in the current working directory'
                                           ' in a file named "differences.txt".  The differences file path and name can'
                                           ' be changed if desired.')
args.add_argument('--file1',
                  type=str,
                  help='The full path and file name of the first file to compare.',
                  required=True)
args.add_argument('--file2',
                  type=str,
                  help='The full path and file name of the second file to compare.',
                  required=True)
args.add_argument('--results',
                  type=str,
                  default=os.getcwd() + '//differences.txt',
                  help='The full path and file name of the file the results will be written to.',
                  required=False)

command_arguments = args.parse_args()

# Setup logging.  Display INFO messages and higher to console
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
log_handler.setLevel(logging.INFO)
logger.addHandler(log_handler)


def main():
    """
    Compare the two supplied files and create a new file that contains a list of all the differences between them.
    """
    logger.debug('\nBegin Comparison...')

    # Setup Files and Paths
    file_1 = command_arguments.file1
    file_2 = command_arguments.file2
    results_file = command_arguments.results

    try:

        # Open source files and split data up for comparison
        with open(file_1, 'r') as data_1:

            source_1 = data_1.read()
            source_1 = source_1.splitlines()

        with open(file_2, 'r') as data_2:

            source_2 = data_2.read()
            source_2 = source_2.splitlines()

        # Create the results file
        with open(results_file, 'w') as results:

            logger.debug('Comparing Data Results')

            # Using difflib return the delta between file_1 and file_2
            for line in difflib.unified_diff(source_1, source_2, fromfile='Solr_3', tofile='Solr_6', n=0):
                results.write(line + '\n')

                logger.debug(line)

    except IOError as e:

        logger.exception('Unable to Open or Write to File')
        logger.exception(e)

    except Exception as e:

        logger.exception('Comparison Of Results Failed')
        logger.exception(e)

if __name__ == '__main__':
    main()

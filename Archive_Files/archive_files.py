#! Python 3
"""
Project:    Utilities
Filename:   archive_files
Created by: PJC
Created on: June 3, 2016
"""

import argparse
import datetime
import logging
import os
import zipfile
from shutil import copyfile

start_time = datetime.datetime.now()

# Get and format string for Archive Name
today = datetime.datetime.today()
formatted_date = today.strftime('%Y%m%d-%H%M')

# Gather arguments which contain paths and file names for the files to be used.
args = argparse.ArgumentParser(prog='archive_files.py',
                               description='This script will archive a supplied directory by zipping up the contents of'
                                           ' that directory.  The archive can be saved to a specific directory or the'
                                           ' current working directory.  If desired, a log of what is archived can be'
                                           ' created and stored with the archived file.')

args.add_argument('--srcdir',
                  type=str,
                  help='The full path of the directory to be archived.',
                  required=True)

args.add_argument('--destdir',
                  type=str,
                  default=os.getcwd(),
                  help='The full path of the directory where the archive will be stored.',
                  required=False)

#  TODO: Need to handle format of the file name better if user doesn't use default
args.add_argument('--zip',
                  type=str,
                  default='archived_files-{0}.zip'.format(formatted_date),
                  help='The file name of the log file.',
                  required=False)

args.add_argument('--ignore',
                  type=str,
                  help='Add a comma separated list of files that should be excluded from the archive.',
                  required=False)

args.add_argument('--log',
                  type=bool,
                  default=False,
                  help='Logging can be added to a file if desired. Set to True to create a log file.  The default '
                       'setting is False.',
                  required=False)

#  TODO: Need to handle format of the file name better if user doesn't use default
args.add_argument('--logfile',
                  type=str,
                  default='archived_files-{0}.log'.format(formatted_date),
                  help='The file name of the log file.',
                  required=False)

command_arguments = args.parse_args()

# Setup logging.  Display INFO messages and higher to console and file log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s-%(message)s', datefmt='%Y/%m/%d %H:%M:%S')

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

if command_arguments.log is True:
    file_handler = logging.FileHandler(dest_dir + command_arguments.logfile)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def main():
    """
    This script zips up a target directory and moves that directory to an archive directory.
    """

    # Assign directories and file names
    working_directory = os.getcwd()
    source_directory = command_arguments.srcdir
    destination_directory = command_arguments.destdir
    root_directory = os.path.dirname(source_directory)
    zip_file_name = command_arguments.zip

    # Separate files to ignore into list for processing
    ignore_string = command_arguments.ignore
    ignore_list = ignore_string.split(",")
    ignore_list = [file_name.strip(' ') for file_name in ignore_list]

    try:
        
        # Create new Zip Archive
        logger.info('Creating {0} in {1}\n'.format(zip_file_name, destination_directory))
        zip_archive = zipfile.ZipFile(destination_directory + '\\' + zip_file_name, mode='w')
    
        # Change the working directory to where the files are
        os.chdir(working_directory)
        
    except Exception:
        
        logger.exception('Creating Zip Archive Failed')
        quit()

    try:
        
        # Walk through directory starting at source_directory and archive files
        for folder, subfolders, files in os.walk(source_directory):

            for file in files:

                # Don't include files that are in the ignore_list
                if file in ignore_list:

                    logger.info('Ignoring {0}...'.format(file))
                    continue

                else:

                    # Add all other files to zip_archive
                    logger.info('Archiving {0}\\{1}...'.format(folder, file))

                    try:

                        #  TODO: Would be nice to only zip relative paths instead of full path
                        zip_archive.write(os.path.join(folder, file), compress_type=zipfile.ZIP_DEFLATED)
                    except PermissionError:

                        logger.warning('Skipping {0} due to PermissionError'.format(file))
        
        logger.info('Closing Archive File\n')

    except Exception:
        
        logger.exception('Problems Adding Files to Archive File')
        
    finally:
        
        # Close the archive file after finished
        zip_archive.close()
        
    logger.info('Script Runtime: {0}\n'.format(str(datetime.datetime.now() - start_time)))

if __name__ == '__main__':
    main()

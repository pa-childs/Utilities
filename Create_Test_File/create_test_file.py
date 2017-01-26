#! python3
"""
Project:    Utilities
Filename:   create_test_file
Created by: PJC
Created on: October 28, 2016
"""

import argparse
import logging
import os

# Setup logging.  Display INFO messages and higher to console
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
log_handler.setLevel(logging.INFO)
logger.addHandler(log_handler)


def main():
    """
    This script will create a file of a specific size.  The file can be used for testing that requires a file
    of a particular size.
    """

    args = argparse.ArgumentParser(prog='create_test_file.py',
                                   description='This script will create a file of a specific size for testing purposes.'
                                               ' The file size and path can be specified as options. The default file'
                                               ' size is 5MB if a size is not provided.  The current working directory'
                                               ' will be the default path if one is not provided. The created file will'
                                               ' be named "test_file-XXMB.dat" where XX is the file size.')
    args.add_argument('-s', type=int, help='The file size in MB.', default=5, required=False)
    args.add_argument('-p', type=str, help='The path where the file is created.', default=os.getcwd(), required=False)

    command_arguments = args.parse_args()

    file_size_in_mb = command_arguments.s
    dir_path = command_arguments.p
    file_name = "test_file-{0}MB.dat".format(str(file_size_in_mb))

    logger.info("Starting To Build File")

    try:

        with open(dir_path + "\\" + file_name, "wb") as fh:
            fh.truncate(1024*1024*file_size_in_mb)

    except Exception:

        logger.exception("Failure In Building File")
        quit()

    logger.info("Finished Building File")
    logger.info("File Location: {0}\{1}".format(dir_path, file_name))
    logger.info("File Size: {0}MB".format(file_size_in_mb))

if __name__ == '__main__':
    main()

#! python3
"""
Project:    Utilities
Filename:   create_test_file
Created by: PJC
Created on: October 28, 2016
"""

import argparse
import colorlog
import logging
import os

# Gather arguments which contain desired file size and path.
args = argparse.ArgumentParser(prog='create_test_file.py',
                               description='This script will create a file of a specific size for testing purposes.'
                                           ' The file size and path can be specified as options. The default file'
                                           ' size is 5MB if a size is not provided.  The current working directory'
                                           ' will be the default path if one is not provided. The created file will'
                                           ' be named "test_file-XXMB.dat" where XX is the file size.')

args.add_argument('--size',
                  type=int,
                  help='The file size in MB.',
                  default=14,
                  required=False)

args.add_argument('--path',
                  type=str,
                  help='The path where the file is created.',
                  default=os.getcwd(),
                  required=False)

command_arguments = args.parse_args()

file_size_in_mb = command_arguments.size
dir_path = command_arguments.path
file_name = "test_file-{0}MB.dat".format(str(file_size_in_mb))

# Setup logging.  Display INFO messages and higher to console
logger = colorlog.getLogger(__name__)
logger.setLevel(colorlog.colorlog.logging.INFO)

log_handler = colorlog.StreamHandler()
log_handler.setFormatter(colorlog.ColoredFormatter())
log_handler.setLevel(logging.INFO)

logger.addHandler(log_handler)


def main():
    """
    This script will create a file of a specific size.  The file can be used for testing that requires a file
    of a particular size.
    """

    logger.info("Starting To Build File")

    try:

        with open(dir_path + "\\" + file_name, "wb") as fh:
            fh.truncate(1024*1024*file_size_in_mb)

    except IOError as e:

        logger.exception('Unable to Open or Write to File')

        logger.exception(e)

    except Exception as e:

        logger.exception("Failure In Building File")
        quit()

    logger.info("Finished Building File")
    logger.info("File Location: {0}\\{1}".format(dir_path, file_name))
    logger.info("File Size: {0}MB".format(file_size_in_mb))


if __name__ == '__main__':
    main()

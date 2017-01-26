#! python3
"""
Project:    Utilities
Filename:   verify_url_links
Created by: PJC
Created on: August 30, 2016
"""

import argparse
import logging
import requests
import time
from datetime import datetime


# Gather arguments which contain paths and file names for the files to be used.
args = argparse.ArgumentParser(prog='verify_url_links.py',
                               description='This script will load a list of URLs from a file and then check the status '
                                           'codes that are returned.  Any Status Codes that is not a 200 will be logged'
                                           'to the screen.')

args.add_argument('--list',
                  type=str,
                  help='The full path and file name of the list of URLs. This is a required argument.',
                  required=True)

args.add_argument('--code',
                  type=str,
                  default='200',
                  help='The HTTP Status Code that is expected to be returned.  Any other code that is returned is '
                       'considered a failure.  This setting defaults to status code 200.',
                  required=False)

args.add_argument('--redir',
                  type=bool,
                  default=True,
                  help='Set whether redirects are allowed.  This setting defaults to True.',
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
    Load all the URLs in the supplied file and confirm they return the supplied Status Code (or 200 if none supplied).
    """
    logger.debug('\nBegin URL Check...')

    start_time = datetime.now()

    # Assign list of URLs to scan
    url_file = command_arguments.LIST
    logger.info('Loading URLs from {0}'.format(command_arguments.LIST))

    # Assign status code to check for
    status_code = command_arguments.CODE
    logger.info('Setting Status Code: {0}'.format(status_code))

    # Determine if Redirects are allowed
    redirects = command_arguments.REDIR
    logger.info('Allowing Redirects: {0}\n'.format(redirects))

    try:

        # Open list of URLs and add data to a list for processing
        with open(url_file, 'r') as url_list:

            target_urls = url_list.read()
            target_urls = target_urls.splitlines()

            logger.info('URLs Ready For Processing\n')

        # Connect for each URL and check the Status Code
        failed_connections = 0
        checked_urls = 0

        logger.info('URLs Checking In Progress\n')
        for url in target_urls:

            # Make request with URL
            logger.info('Checking {0}'.format(url))
            response = requests.get(url, allow_redirects=redirects)

            # Check status and return result
            if response.status_code != status_code:

                failed_connections += 1
                logger.warn('Failure: {0} returned a Status Code of {1}'.format(url, response.status_code))

            else:

                logger.info('Success: {0} returned a Status Code of {1}'.format(url, response.status_code))

            checked_urls += 1

            # Pause to prevent annoying Rack Attack
            time.sleep(2)

    except KeyboardInterrupt:

        # Finish up after a Ctrl-C interrupts script
        logger.warn('URL checking interrupted by user.  Scanned totals are incomplete...')

    except IOError as e:

        logger.exception('Could Not Open URL File')
        logger.exception(e)

    finally:

        logger.info('Number of URLs checked: {0}'.format(checked_urls))
        logger.info('Number of failed connections: {0}'.format(failed_connections))

    logger.info('Runtime = {0}'.format(datetime.now() - start_time))

if __name__ == '__main__':
    main()

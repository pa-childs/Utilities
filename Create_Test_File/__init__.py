#! python3
"""
Project:    Sandbox
Filename:   __init__.py
Created by: PJC
Created on: October 28, 2016
"""

import logging

# Setup logging.  Display INFO messages and higher to console
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
log_handler.setLevel(logging.INFO)
logger.addHandler(log_handler)


def main():
    pass


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_cleanup.py

    Description:  Clean up of log and message files in test environment for
        blackbox testing.

    Usage:  blackbox_cleanup.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Third-party
import glob

# Local
sys.path.append(os.getcwd())
import version

__version__ = version.__version__


def delete_files(base_dir, f_filter):

    """Function:  delete_files

    Description:  Delete test files in base directory with passed file filter.

    Arguments:
        (input) base_dir -> Base directory path to testing directory.
        (input) f_filter -> File filter for searching.

    """

    for item in glob.glob(os.path.join(base_dir, f_filter)):
        os.remove(item)


def main():

    """Function:  main

    Description:  Controls flow of program.

    Variables:

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    sysmon_dir = os.path.join(test_path, "sysmon")
    message_dir = os.path.join(test_path, "message_dir")
    logs_dir = os.path.join(test_path, "logs")
    delete_files(logs_dir, "rmq_2_sysmon*.log")
    delete_files(message_dir, "blackbox-test_blackbox-test_*.txt")
    delete_files(sysmon_dir, "*.json")


if __name__ == "__main__":
    sys.exit(main())

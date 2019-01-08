#!/usr/bin/python
# Classification (U)

###############################################################################
#
# Program:      blackbox_test.py
#
# Class Dependencies:
#               class.rabbitmq_class    => v0.3.0 or higher
#
# Library Dependenices:
#               lib.gen_libs            => v2.4.0 or higher
#               blackbox_libs           => v0.2.0 or higher
#
###############################################################################

"""Program:  blackbox_test.py

    Description:  Blackbox testing of rmq_2_sysmon.py program.

    Usage:
        test/blackbox/rmq_2_sysmon/blackbox_test.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Third-party
import json
import glob
import ast

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import blackbox_libs
import version

# Version Information
__version__ = version.__version__


def test_1(RQ, file_path, message_dir, log_dir, **kwargs):

    """Function:  test_1

    Description:  Process a single properly formatted message.

    Arguments:
        (input) RQ -> RabbitMQ Publisher instance
        (input) file_path -> Directory path to test file location.
        (input) message_dir -> Directory path to location of error messages.
        (input) log_dir -> Directory path to location of log file.
        (input) **kwargs:
            None

    """

    print("\tTest 1:  Process non-sysmon report.")
    f_name = "SERVER_NAME2"
    key = "Server"
    msg = "Dictionary does not contain key"
    f_filter = "blackbox-test_blackbox-test*.txt"
    f_filter2 = "rmq_2_sysmon*.log"

    status, err_msg = blackbox_libs.publish_msg(RQ,
                                                os.path.join(file_path,
                                                             f_name + ".txt"))

    time.sleep(1)

    if status:
        for f_file in glob.glob(os.path.join(message_dir, f_filter)):
            with open(f_file, "r") as f_hldr:
                body = f_hldr.read()

            data = ast.literal_eval(body.splitlines()[1])
            break

        for f_file in glob.glob(os.path.join(log_dir, f_filter2)):
            with open(f_file, "r") as f_hldr:
                msg_body = f_hldr.read()

        if key not in data and msg in msg_body:
            print("\tTest successful\n")

        else:
            print("Error: Incorrect data file or log file entry.")
            print("\tTest failed\n")

    else:
        print("Error Message:  %s" % (err_msg))
        print("Error:  Failed to publish message to RabbitMQ\n")


def main():

    """Function:  main

    Description:  Control the blackbox testing of rmq_2_sysmon.py program.

    Variables:
        base_dir -> Directory path to blackbox testing directory.
        test_path -> Current full directory path, including base_dir.
        config_path -> Directory path to config, including test_path.
        file_path -> Directory path the test files.

    Arguments:
        None

    """

    base_dir = "test/blackbox/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    file_path = os.path.join(test_path, "testfiles")
    cfg = gen_libs.load_module("rabbitmq", config_path)

    RQ = blackbox_libs.create_rq_pub(cfg)

    if RQ:
        test_1(RQ, file_path, cfg.message_dir, cfg.log_dir)

    else:
        print("Error:  Failed to create RabbitMQ Publisher instance")


if __name__ == "__main__":
    sys.exit(main())

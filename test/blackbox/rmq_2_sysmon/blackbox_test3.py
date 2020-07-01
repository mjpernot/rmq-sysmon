#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test.py

    Description:  Blackbox testing of rmq_2_sysmon.py program.

    Usage:
        test/blackbox/rmq_2_sysmon/blackbox_test.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Third-party
import glob

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import blackbox_libs
import version

__version__ = version.__version__


def test_1(rmq, file_path, message_dir, log_dir):

    """Function:  test_1

    Description:  Process a non-type report.

    Arguments:
        (input) rmq -> RabbitMQ Publisher instance
        (input) file_path -> Directory path to test file location.
        (input) message_dir -> Directory path to location of error messages.
        (input) log_dir -> Directory path to location of log file.

    """

    print("\tTest 1:  Process non-type report.")
    f_name = "SERVER_NAME2"
    msg = "Incorrect type"
    f_filter = "blackbox-test_blackbox-test"
    f_filter2 = "rmq_2_sysmon*.log"
    status, err_msg = blackbox_libs.publish_msg(
        rmq, os.path.join(file_path, f_name + ".txt"))
    time.sleep(1)

    if status:
        f_file = gen_libs.dir_file_match(message_dir, f_filter,
                                         add_path=True)[0]

        for item in glob.glob(os.path.join(log_dir, f_filter2)):
            with open(item, "r") as f_hldr:
                msg_body = f_hldr.read()

        if os.path.isfile(f_file) and msg in msg_body:
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

    """

    base_dir = "test/blackbox/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    file_path = os.path.join(test_path, "testfiles")
    cfg = gen_libs.load_module("rabbitmq", config_path)
    rmq = blackbox_libs.create_rq_pub(cfg)

    if rmq:
        test_1(rmq, file_path, cfg.message_dir, cfg.log_dir)

    else:
        print("Error:  Failed to create RabbitMQ Publisher instance")


if __name__ == "__main__":
    sys.exit(main())

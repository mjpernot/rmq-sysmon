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

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import blackbox_libs
import version

__version__ = version.__version__


def test_1(rmq, file_path, sysmon_dir):

    """Function:  test_1

    Description:  Process a single properly formatted message.

    Arguments:
        (input) rmq -> RabbitMQ Publisher instance
        (input) file_path -> Directory path to test file location.
        (input) sysmon_dir -> Directory path to location of sysmon reports.

    """

    print("\tTest 1:  Process formatted sysmon report.")
    f_name = "SERVER_NAME"
    status, err_msg = blackbox_libs.publish_msg(
        rmq, os.path.join(file_path, f_name + ".txt"))
    time.sleep(1)

    if status:
        status, err_msg = \
            blackbox_libs.file_test(os.path.join(
                sysmon_dir, f_name + "_pkgs.json"))

        if status:
            print("\tTest successful\n")

        else:
            print("Error Message:  %s" % (err_msg))
            print("\tTest failed\n")

        os.remove(os.path.join(sysmon_dir, f_name + "_pkgs.json"))

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
        test_1(rmq, file_path, cfg.queue_list[0]["directory"])

    else:
        print("Error:  Failed to create RabbitMQ Publisher instance")


if __name__ == "__main__":
    sys.exit(main())

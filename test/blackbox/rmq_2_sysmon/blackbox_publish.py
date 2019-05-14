#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_publish.py

    Description:  Blackbox testing of rmq_2_sysmon.py program.

    Usage:
        test/blackbox/rmq_2_sysmon/blackbox_publish.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Third-party

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import blackbox_libs
import version

# Version Information
__version__ = version.__version__


def test_1(rq, file_path, **kwargs):

    """Function:  test_1

    Description:  Publish test message to RabbitMQ queue.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) file_path -> Directory path to test file location.
        (input) **kwargs:
            None

    """

    f_name = "SERVER_NAME"
    status, err_msg = blackbox_libs.publish_msg(rq,
                                                os.path.join(file_path,
                                                             f_name + ".txt"))

    if not status:
        print("Error Message:  %s" % (err_msg))
        print("Error:  Publish failed\n")


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
    rq = blackbox_libs.create_rq_pub(cfg)

    if rq:
        test_1(rq, file_path)

    else:
        print("Error:  Failed to create RabbitMQ Publisher instance")


if __name__ == "__main__":
    sys.exit(main())

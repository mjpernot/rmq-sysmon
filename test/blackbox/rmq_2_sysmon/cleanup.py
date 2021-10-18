#!/usr/bin/python
# Classification (U)

"""Program:  cleanup.py

    Description:  Clean up of test files in environment and cleanup of
        RabbitMQ exchange and queues.

    Usage:
        test/blackbox/rmq_2_sysmon/cleanup.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Third-party

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import blackbox_cleanup
import rmq_cleanup
import version

__version__ = version.__version__


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
    config_path = os.path.join(test_path, "config")
    cfg = gen_libs.load_module("rabbitmq", config_path)
    blackbox_cleanup.delete_files(logs_dir, "rmq_2_sysmon*.log")
    blackbox_cleanup.delete_files(message_dir,
                                  "blackbox-test_blackbox-test_*.txt")
    blackbox_cleanup.delete_files(sysmon_dir, "*.json")
    rmq_cleanup.rmq_cleanup(cfg, cfg.queue_list[0]["queue"], True)


if __name__ == "__main__":
    sys.exit(main())

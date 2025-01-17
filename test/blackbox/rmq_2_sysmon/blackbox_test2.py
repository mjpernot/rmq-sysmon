#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test2.py

    Description:  Blackbox testing of rmq_2_sysmon.py program.

    Usage:
        test/blackbox/rmq_2_sysmon/blackbox_test2.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Local
sys.path.append(os.getcwd())
import blackbox_libs                            # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def test_1(sysmon_dir):

    """Function:  test_1

    Description:  Test:  Process message already in queue.

    Arguments:
        (input) sysmon_dir -> Directory path to location of sysmon reports.

    """

    print("\tTest 1:  Process message already in queue")
    f_name = "SERVER_NAME"
    time.sleep(1)
    status, err_msg = \
        blackbox_libs.file_test(
            os.path.join(sysmon_dir, f_name + "_pkgs.json"))

    if status:
        print("\tTest successful\n")

    else:
        print(f"Error Message:  {err_msg}")
        print("\tTest failed\n")

    os.remove(os.path.join(sysmon_dir, f_name + "_pkgs.json"))


def main():

    """Function:  main

    Description:  Control the blackbox testing of rmq_2_sysmon.py program.

    Variables:
        base_dir -> Directory path to blackbox testing directory.
        test_path -> Current full directory path, including base_dir.
        config_path -> Directory path to config, including test_path.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    cfg = gen_libs.load_module("rabbitmq", config_path)
    test_1(cfg.queue_list[0]["directory"])


if __name__ == "__main__":
    sys.exit(main())

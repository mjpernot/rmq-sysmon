#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/run_program.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_sysmon
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def monitor_queue(cfg, log):

    """Function Stub:  monitor_queue

    Description:  This is a function stub for rmq_2_sysmon.monitor_queue

    Arguments:
        cfg -> Stub argument holder.
        log -> Stub argument holder.

    """

    status = True

    if cfg and log:
        status = True

    return status


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline -> Argv command line.
            (input) flavor -> Lock flavor ID.

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_status_false -> Test with status is False.
        test_status_true -> Test with status is True.
        test_func_call -> Test with call to function.
        test_raise_exception -> Test with raising exception.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.host = "SERVER_NAME"
                self.exchange_name = "EXCHANGE_NAME"
                self.log_file = "LOG_FILE"
                self.to_line = "TO_LINE"
                self.queue_list = [
                    {"queue": "QUEUE_NAME",
                     "routing_key": "ROUTING_KEY"}]

        self.cfg = CfgTest()
        self.proglock = ProgramLock(["cmdline"], "FlavorID")
        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.func_dict = {"-M": monitor_queue}

    @mock.patch("rmq_2_sysmon.validate_create_settings")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_status_false(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_false

        Description:  Test run_program function with status is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_load.return_value = self.cfg
        mock_valid.return_value = (self.cfg, False, "Failed to load cfg")

        with gen_libs.no_std_out():
            self.assertFalse(rmq_2_sysmon.run_program(self.args,
                                                      self.func_dict))

    @mock.patch("rmq_2_sysmon.validate_create_settings")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_status_true(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_true

        Description:  Test run_program function with status is True.

        Arguments:

        """

        mock_log.return_value = rmq_2_sysmon.gen_class.Logger
        mock_load.return_value = self.cfg
        mock_valid.return_value = (self.cfg, True, "")
        mock_log.log_close.return_value = True

        # Remove to skip "for" loop.
        self.args.pop("-M")

        self.assertFalse(rmq_2_sysmon.run_program(self.args, self.func_dict))

    @mock.patch("rmq_2_sysmon.monitor_queue")
    @mock.patch("rmq_2_sysmon.validate_create_settings")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.gen_class")
    def test_func_call(self, mock_class, mock_load, mock_valid, mock_func):

        """Function:  test_func_call

        Description:  Test run_program function with call to function.

        Arguments:

        """

        mock_class.Logger.return_value = rmq_2_sysmon.gen_class.Logger
        mock_load.return_value = self.cfg
        mock_valid.return_value = (self.cfg, True, "")
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock.return_value = self.proglock
        mock_func.return_value = True

        self.assertFalse(rmq_2_sysmon.run_program(self.args, self.func_dict))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.validate_create_settings")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.gen_class.ProgramLock")
    def test_raise_exception(self, mock_lock, mock_load, mock_valid, mock_log):

        """Function:  test_raise_exception

        Description:  Test run_program function with raising the exception.

        Arguments:

        """

        mock_lock.side_effect = rmq_2_sysmon.gen_class.SingleInstanceException
        mock_log.return_value = rmq_2_sysmon.gen_class.Logger
        mock_log.log_info.return_value = True
        mock_log.log_close.return_value = True
        mock_load.return_value = self.cfg
        mock_valid.return_value = (self.cfg, True, "")

        self.assertFalse(rmq_2_sysmon.run_program(self.args, self.func_dict))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.cfg = None


if __name__ == "__main__":
    unittest.main()

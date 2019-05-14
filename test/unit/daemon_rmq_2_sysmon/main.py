#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in daemon_rmq_2_sysmon.py.

    Usage:
        test/unit/daemon_rmq_2_sysmon/main.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import daemon_rmq_2_sysmon
import lib.gen_libs as gen_libs
import version

# Version Information
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        test_start_daemon -> Test main function with daemon start option.
        test_stop_daemon -> Test main function with daemon stop option.
        test_restart_daemon -> Test main function with daemon restart option.
        test_invalid_daemon -> Test main function with invalid option.
        test_arg_require_false -> Test main function with arg_require false.
        test_arg_require_true -> Test main function with arg_require true.

    """

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start")
    def test_start_daemon(self, mock_daemon, mock_arg):

        """Function:  test_start_daemon

        Description:  Test main function with daemon start option.

        Arguments:
            mock_daemon -> Mock Ref:  daemon_rmq_2_sysmon.Rmq2SysmonDaemon
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "start", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.stop")
    def test_stop_daemon(self, mock_daemon, mock_arg):

        """Function:  test_stop_daemon

        Description:  Test main function with daemon stop option.

        Arguments:
            mock_daemon -> Mock Ref:  daemon_rmq_2_sysmon.Rmq2SysmonDaemon
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "stop", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.restart")
    def test_restart_daemon(self, mock_daemon, mock_arg):

        """Function:  test_restart_daemon

        Description:  Test main function with daemon restart option.

        Arguments:
            mock_daemon -> Mock Ref:  daemon_rmq_2_sysmon.Rmq2SysmonDaemon
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "restart", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_invalid_daemon(self, mock_arg):

        """Function:  test_invalid_daemon

        Description:  Test main function with invalid option.

        Arguments:
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "nostart", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start")
    def test_arg_require_false(self, mock_daemon, mock_arg):

        """Function:  test_arg_require_false

        Description:  Test main function with arg_require false.

        Arguments:
            mock_daemon -> Mock Ref:  daemon_rmq_2_sysmon.Rmq2SysmonDaemon
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "start", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_arg_require_true(self, mock_arg):

        """Function:  test_arg_require_true

        Description:  Test main function with arg_require true.

        Arguments:
            mock_arg -> Mock Ref:  daemon_rmq_2_sysmon.arg_parser

        """

        args = {"-a": "start", "-c": "rabbitmq"}
        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = True

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)


if __name__ == "__main__":
    unittest.main()

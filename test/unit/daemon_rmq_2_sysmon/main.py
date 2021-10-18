#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in daemon_rmq_2_sysmon.py.

    Usage:
        test/unit/daemon_rmq_2_sysmon/main.py

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
import daemon_rmq_2_sysmon
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_start_remove
        test_start_exists
        test_pid_not_running
        test_pid_running
        test_start_daemon
        test_stop_daemon
        test_restart_daemon
        test_invalid_daemon
        test_arg_require_false
        test_arg_require_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = {"-a": "start", "-c": "rabbitmq"}

    @mock.patch("daemon_rmq_2_sysmon.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.is_active",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_start_remove(self, mock_arg):

        """Function:  test_start_remove

        Description:  Test with daemon start option, but pid file exist.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.is_active",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_start_exists(self, mock_arg):

        """Function:  test_start_exists

        Description:  Test with daemon start option, but already running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.is_active", mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_pid_not_running(self, mock_arg):

        """Function:  test_pid_not_running

        Description:  Test with pid file and process not running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.is_active", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_pid_running(self, mock_arg):

        """Function:  test_pid_running

        Description:  Test with pid file and process running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_start_daemon(self, mock_arg):

        """Function:  test_start_daemon

        Description:  Test main function with daemon start option.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.stop")
    def test_stop_daemon(self, mock_daemon, mock_arg):

        """Function:  test_stop_daemon

        Description:  Test main function with daemon stop option.

        Arguments:

        """

        self.args["-a"] = "stop"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.restart")
    def test_restart_daemon(self, mock_daemon, mock_arg):

        """Function:  test_restart_daemon

        Description:  Test main function with daemon restart option.

        Arguments:

        """

        self.args["-a"] = "restart"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_invalid_daemon(self, mock_arg):

        """Function:  test_invalid_daemon

        Description:  Test main function with invalid option.

        Arguments:

        """

        self.args["-a"] = "nostart"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_2_sysmon.Rmq2SysmonDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_arg_require_false(self, mock_arg):

        """Function:  test_arg_require_false

        Description:  Test main function with arg_require false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)

    @mock.patch("daemon_rmq_2_sysmon.arg_parser")
    def test_arg_require_true(self, mock_arg):

        """Function:  test_arg_require_true

        Description:  Test main function with arg_require true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = True

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_sysmon.main)


if __name__ == "__main__":
    unittest.main()

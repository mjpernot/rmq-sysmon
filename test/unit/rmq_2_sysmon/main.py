# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/main.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_sysmon
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_dir_chk
        arg_require

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()
        self.opt_req = None
        self.opt_req2 = True
        self.dir_perms_chk = None
        self.dir_perms_chk2 = True

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_true
        test_help_false
        test_require_false
        test_require_true
        test_dir_chk_crt_false
        test_dir_chk_crt_true
        test_run_program

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array = {
            "-c": "config_file", "-d": "config_dir", "-M": True}

    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_status_true

        Description:  Test main function with Help_Func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_status_false

        Description:  Test main function with Help_Func returns False.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_require_false(self, mock_arg, mock_help):

        """Function:  test_require_false

        Description:  Test with arg_require returns False.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_require_true(self, mock_arg, mock_help):

        """Function:  test_require_true

        Description:  Test with arg_require returns True.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_dir_chk_crt_false(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_false

        Description:  Test with arg_dir_chk_crt returns False.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.run_program", mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_dir_chk_crt_true(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_true

        Description:  Test with arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())

    @mock.patch("rmq_2_sysmon.run_program", mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_libs.help_func")
    @mock.patch("rmq_2_sysmon.gen_class.ArgParser")
    def test_run_program(self, mock_arg, mock_help):

        """Function:  test_run_program

        Description:  Test with run_program.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_2_sysmon.main())


if __name__ == "__main__":
    unittest.main()

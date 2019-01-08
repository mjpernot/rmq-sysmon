#!/usr/bin/python
# Classification (U)

###############################################################################
#
# Program:      validate_create_settings.py
#
# Class Dependencies:
#               None
#
# Library Dependenices:
#               rmq_2_sysmon    => 0.0.1 or higher
#               lib/gen_libs    => 2.4.0 or higher
#
###############################################################################

"""Program:  validate_create_settings.py

    Description:  Unit testing of validate_create_settings in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/validate_create_settings.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import datetime

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_sysmon
import version
import lib.gen_libs as gen_libs

# Version Information
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Initialize testing environment.
        test_multiple_false2 -> Test if multiple checks return False.
        test_multiple_false -> Test if multiple checks return False.
        test_sysmon_dir_true -> Test if sysmon_dir check returns True.
        test_log_dir_false -> Test if log_dir check returns False.
        test_log_dir_true -> Test if log_dir check returns True.
        test_message_dir_false -> Test if message_dir check returns False.
        test_message_dir_true -> Test if message_dir check returns True.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        self.base_dir = "test/unit/rmq_2_sysmon"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", self.config_path)
        self.err_msg1 = "Missing Message Dir "
        self.err_msg2 = "Missing Log Dir "
        self.err_msg3 = "Missing Sysmon Dir "

        base_name, ext_name = os.path.splitext(self.cfg.log_file)
        self.log_name = base_name + "_" + self.cfg.exchange_name + "_" \
            + self.cfg.queue_name + ext_name

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_multiple_false2(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (False, self.err_msg2),
                                            (False, self.err_msg3)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False,
                          self.err_msg1 + self.err_msg2 + self.err_msg3))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_multiple_false(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (False, self.err_msg2),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False, self.err_msg1 + self.err_msg2))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_sysmon_dir_false(self, mock_lib):

        """Function:  test_sysmon_dir_false

        Description:  Test if sysmon_dir check returns False.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg3),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg3))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_sysmon_dir_true(self, mock_lib):

        """Function:  test_sysmon_dir_true

        Description:  Test if sysmon_dir check returns True.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_log_dir_false(self, mock_lib):

        """Function:  test_log_dir_false

        Description:  Test if log_dir check returns False.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg2),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg2))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_log_dir_true(self, mock_lib):

        """Function:  test_log_dir_true

        Description:  Test if log_dir check returns True.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg, cfg_mod.log_file),
                         (True, "", os.path.join(self.cfg.log_dir,
                                                 self.log_name)))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_message_dir_false(self, mock_lib):

        """Function:  test_message_dir_false

        Description:  Test if message_dir check returns False.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (True, None), (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg1))

    @mock.patch("rmq_2_sysmon.gen_libs")
    def test_message_dir_true(self, mock_lib):

        """Function:  test_message_dir_true

        Description:  Test if message_dir check returns True.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_sysmon.gen_libs

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None)]

        cfg_mod, status_flag, err_msg = \
            rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()

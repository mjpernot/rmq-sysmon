#!/usr/bin/python
# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Integration testing of validate_create_settings in
        rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/validate_create_settings.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_sysmon_dir_chk_false
        test_log_dir_chk_false
        test_msg_dir_chk_false
        test_sysmon_dir_chk_true
        test_log_dir_chk_true
        test_msg_dir_chk_true
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:

        """

        self.base_dir = "test/integration/rmq_2_sysmon"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", self.config_path)
        log_path = os.path.join(self.test_path, self.cfg.log_dir)
        self.cfg.log_file = os.path.join(log_path, self.cfg.log_file)
        self.cfg.queue_list[0]["directory"] = \
            os.path.join(self.test_path, self.cfg.queue_list[0]["directory"])
        self.message_dir = os.path.join(self.test_path, self.cfg.message_dir)
        self.log_dir = os.path.join(self.test_path, self.cfg.log_dir)
        self.sysmon_dir = os.path.join(self.test_path,
                                       self.cfg.queue_list[0]["directory"])
        self.msg = " does not exist."
        self.msg2 = "Error: Directory: "
        self.msg3 = " is not writeable."
        self.msg4 = " is not readable."
        self.msg5 = "Error: Directory "

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_sysmon_dir_chk_false(self, mock_base):

        """Function:  test_sysmon_dir_chk_false

        Description:  Test gen_libs.chk_crt_dir(sysmon_dir) is False.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg.queue_list[0]["directory"] = os.path.join(
            self.test_path, self.cfg.queue_list[0]["directory"] + "FALSE")
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)
        t_msg = self.msg2 + self.cfg.queue_list[0]["directory"] + self.msg
        t_msg = t_msg + "\n" + self.msg5 \
            + self.cfg.queue_list[0]["directory"] + self.msg3
        t_msg = t_msg + "\n" + self.msg5 \
            + self.cfg.queue_list[0]["directory"] + self.msg4

        self.assertEqual((self.cfg.queue_list[0]["directory"], status, msg),
                         (self.sysmon_dir + "FALSE", False, t_msg))

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_log_dir_chk_false(self, mock_base):

        """Function:  test_log_dir_chk_false

        Description:  Test gen_libs.chk_crt_dir(log_dir) is False.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg.log_dir = os.path.join(self.test_path,
                                        self.cfg.log_dir + "FALSE")
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)
        t_msg = self.msg2 + self.cfg.log_dir + self.msg
        t_msg = t_msg + "\n" + self.msg5 + self.cfg.log_dir + self.msg3
        t_msg = t_msg + "\n" + self.msg5 + self.cfg.log_dir + self.msg4

        self.assertEqual((self.cfg.log_dir, status, msg),
                         (self.log_dir + "FALSE", False, t_msg))

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_msg_dir_chk_false(self, mock_base):

        """Function:  test_msg_dir_chk_false

        Description:  Test gen_libs.chk_crt_dir(message_dir) is False.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg.message_dir = os.path.join(self.test_path,
                                            self.cfg.message_dir + "FALSE")
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)
        t_msg = self.msg2 + self.cfg.message_dir + self.msg
        t_msg = t_msg + "\n" + self.msg5 + self.cfg.message_dir + self.msg3
        t_msg = t_msg + "\n" + self.msg5 + self.cfg.message_dir + self.msg4

        self.assertEqual((self.cfg.message_dir, status, msg),
                         (self.message_dir + "FALSE", False, t_msg))

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_sysmon_dir_chk_true(self, mock_base):

        """Function:  test_sysmon_dir_chk_true

        Description:  Test gen_libs.chk_crt_dir(sysmon_dir) is True.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((self.cfg.queue_list[0]["directory"], status, msg),
                         (self.sysmon_dir, True, ""))

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_log_dir_chk_true(self, mock_base):

        """Function:  test_log_dir_chk_true

        Description:  Test gen_libs.chk_crt_dir(log_dir) is True.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((self.cfg.log_dir, status, msg),
                         (self.log_dir, True, ""))

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    def test_msg_dir_chk_true(self, mock_base):

        """Function:  test_msg_dir_chk_true

        Description:  Test gen_libs.chk_crt_dir(message_dir) is True.

        Arguments:

        """

        mock_base.return_value = self.test_path
        self.cfg, status, msg = rmq_2_sysmon.validate_create_settings(self.cfg)

        self.assertEqual((self.cfg.message_dir, status, msg),
                         (self.message_dir, True, ""))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()

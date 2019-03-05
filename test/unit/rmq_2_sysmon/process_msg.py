#!/usr/bin/python
# Classification (U)

"""Program:  process_msg.py

    Description:  Unit testing of process_msg in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/process_msg.py

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
        test_key_not_in_dict -> Test if key is not in dictionary.
        test_create_json_fail -> Test if the body is unable to convert to JSON.
        test_create_json -> Test if the body is converted to JSON.
        test_is_dict -> Test if the body is a dictionary.
        test_is_not_dict -> Test if the body is not a dictionary.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:
                        None

                """

                self.host = "HOSTNAME"
                self.sysmon_dir = "/SYSMON_DIR_PATH"
                self.exchange_name = "rmq_2_isse_unit_test"
                self.queue_name = "rmq_2_isse_unit_test"
                self.to_line = None
                self.transfer_dir = "/TRANSFER_DIR_PATH"
                self.isse_dir = "/ISSE_DIR_PATH"
                self.delta_month = 6
                self.port = 5672
                self.exchange_type = "direct"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = False
                self.message_dir = "message_dir"
                self.log_dir = "logs"
                self.log_file = "rmq_2_isse.log"
                self.proc_file = "files_processed"
                self.ignore_ext = ["_kmz.64.txt", "_pptx.64.txt"]

        self.cfg = CfgTest()

        self.base_dir = "/BASE_DIR_PATH"
        self.method = "Method Properties"
        self.body = {"Server": "SERVER_NAME.domain.name"}
        self.body2 = {"Non-Key": "Non-Value"}
        self.rq = "RabbitMQ Instance"

    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.json.loads")
    def test_key_not_in_dict(self, mock_json, mock_log, mock_msg):

        """Function:  test_create_json_fail

        Description:  Test if the body is unable to convert to JSON.

        Arguments:
            mock_json -> Mock Ref:  rmq_2_sysmon.json.loads
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_msg -> Mock Ref:  rmq_2_sysmon.non_proc_msg

        """

        mock_json.return_value = self.body2
        mock_log.return_value = True
        mock_msg.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rq, mock_log, self.cfg,
                                                  self.method, self.body2))

    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.gen_libs.print_dict")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.json.loads")
    def test_create_json_fail(self, mock_json, mock_log, mock_libs, mock_msg):

        """Function:  test_create_json_fail

        Description:  Test if the body is unable to convert to JSON.

        Arguments:
            mock_json -> Mock Ref:  rmq_2_sysmon.json.loads
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_libs -> Mock Ref:  rmq_2_sysmon.gen_libs.print_dict
            mock_msg -> Mock Ref:  rmq_2_sysmon.non_proc_msg

        """

        mock_json.return_value = self.body
        mock_log.return_value = True
        mock_libs.return_value = (True, "Unable to convert to JSON")
        mock_msg.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_libs.print_dict")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.json.loads")
    def test_create_json(self, mock_json, mock_log, mock_libs):

        """Function:  test_create_json

        Description:  Test if the body is converted to JSON.

        Arguments:
            mock_json -> Mock Ref:  rmq_2_sysmon.json.loads
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_libs -> Mock Ref:  rmq_2_sysmon.gen_libs.print_dict

        """

        mock_json.return_value = self.body
        mock_log.return_value = True
        mock_libs.return_value = (False, "")

        self.assertFalse(rmq_2_sysmon.process_msg(self.rq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_libs.print_dict")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.json.loads")
    def test_is_dict(self, mock_json, mock_log, mock_libs):

        """Function:  test_is_dict

        Description:  Test if the body is a dictionary.

        Arguments:
            mock_json -> Mock Ref:  rmq_2_sysmon.json.loads
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_libs -> Mock Ref:  rmq_2_sysmon.gen_libs.print_dict

        """

        mock_json.return_value = self.body
        mock_log.return_value = True
        mock_libs.return_value = (False, "")

        self.assertFalse(rmq_2_sysmon.process_msg(self.rq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.json.loads")
    def test_is_not_dict(self, mock_json, mock_msg, mock_log):

        """Function:  test_is_not_dict

        Description:  Test if the body is not a dictionary.

        Arguments:
            mock_json -> Mock Ref:  rmq_2_sysmon.json.loads
            mock_msg -> Mock Ref:  rmq_2_sysmon.non_proc_msg
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger

        """

        mock_json.return_value = ["Key", "Value"]
        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rq, mock_log, self.cfg,
                                                  self.method, self.body))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        pass


if __name__ == "__main__":
    unittest.main()

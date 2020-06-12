#!/usr/bin/python
# Classification (U)

"""Program:  process_msg.py

    Description:  Unit testing of process_msg in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/process_msg.py

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
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_str_convert_pass -> Test with ast.literal_eval pass for string.
        test_dict_convert_pass -> Test with ast.literal_eval pass for dict.
        test_str_convert_fails -> Test with ast.literal_eval fails for string.
        test_dict_convert_fails -> Test with ast.literal_eval fails for dict.
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
                self.prename = "Pre-filename"
                self.postname = "Post-filename"
                self.key = "Server"

        self.cfg = CfgTest()
        self.base_dir = "/BASE_DIR_PATH"
        self.method = "Method Properties"
        self.body = {"Server": "SERVER_NAME.domain.name"}
        self.body2 = {"Non-Key": "Non-Value"}
        self.body3 = "This a string"
        self.rawbody2 = '{"Non-Key": "Non-Value"}'
        self.rawbody3 = '"This a string"'
        self.rmq = "RabbitMQ Instance"

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_str_convert_pass(self, mock_msg, mock_log):

        """Function:  test_str_convert_pass

        Description:  Test with ast.literal_eval pass for string.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.rawbody3))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_dict_convert_pass(self, mock_msg, mock_log):

        """Function:  test_dict_convert_pass

        Description:  Test with ast.literal_eval pass for dict.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.rawbody2))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_str_convert_fails(self, mock_msg, mock_log):

        """Function:  test_str_convert_fails

        Description:  Test with ast.literal_eval fails for string.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body3))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_dict_convert_fails(self, mock_msg, mock_log):

        """Function:  test_dict_convert_fails

        Description:  Test with ast.literal_eval fails for dict.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body2))

    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_key_not_in_dict(self, mock_json, mock_log, mock_msg):

        """Function:  test_create_json_fail

        Description:  Test if the body is unable to convert to JSON.

        Arguments:

        """

        mock_json.return_value = self.body2
        mock_log.return_value = True
        mock_msg.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body2))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_create_json_fail(self, mock_json, mock_log, mock_msg):

        """Function:  test_create_json_fail

        Description:  Test if the body is unable to convert to JSON.

        Arguments:

        """

        mock_json.return_value = self.body
        mock_log.return_value = True
        mock_msg.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_create_json(self, mock_json, mock_log):

        """Function:  test_create_json

        Description:  Test if the body is converted to JSON.

        Arguments:

        """

        mock_json.return_value = self.body
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_is_dict(self, mock_json, mock_log):

        """Function:  test_is_dict

        Description:  Test if the body is a dictionary.

        Arguments:

        """

        mock_json.return_value = self.body
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body))

    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_is_not_dict(self, mock_json, mock_msg, mock_log):

        """Function:  test_is_not_dict

        Description:  Test if the body is not a dictionary.

        Arguments:

        """

        mock_json.return_value = ["Key", "Value"]
        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(self.rmq, mock_log, self.cfg,
                                                  self.method, self.body))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        pass


if __name__ == "__main__":
    unittest.main()

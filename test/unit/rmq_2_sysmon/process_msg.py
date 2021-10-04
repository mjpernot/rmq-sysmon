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
        setUp
        test_no_routing_key
        test_default_name
        test_no_postname
        test_postname
        test_no_prename
        test_prename
        test_date_true
        test_date_false
        test_dtg_true
        test_dtg_false
        test_flatten_false
        test_flatten_true
        test_ext_set
        test_no_dict_key_set
        test_no_dict_key_pass
        test_any_pass
        test_str_pass
        test_list_pass
        test_str_convert_pass
        test_dict_convert_pass
        test_convert_fails_type_pass
        test_str_convert_fails
        test_dict_convert_fails
        test_key_not_in_dict
        test_create_json_fail
        test_create_json
        test_is_dict
        test_is_not_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class MethodTest(object):

            """Class:  MethodTest

            Description:  Class which is a representation of a method module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.routing_key = "ROUTING_KEY"

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
                self.exchange_name = "rmq_2_isse_unit_test"
                self.to_line = None
                self.port = 5672
                self.exchange_type = "direct"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = False
                self.message_dir = "message_dir"
                self.log_dir = "logs"
                self.log_file = "rmq_2_isse.log"
                self.queue_list = [
                    {"queue": "rmq_2_isse_unit_test",
                     "routing_key": "ROUTING_KEY",
                     "directory": "/SYSMON_DIR_PATH",
                     "prename": "Pre-filename",
                     "postname": "Post-filename",
                     "key": "Server",
                     "mode": "a",
                     "ext": "",
                     "dtg": False,
                     "date": False,
                     "stype": "dict",
                     "flatten": True}]

        self.cfg = CfgTest()
        self.cfg2 = CfgTest()
        self.cfg2.queue_list[0]["stype"] = "list"
        self.cfg3 = CfgTest()
        self.cfg3.queue_list[0]["stype"] = "str"
        self.cfg4 = CfgTest()
        self.cfg4.queue_list[0]["stype"] = "any"
        self.cfg5 = CfgTest()
        self.cfg5.queue_list[0]["key"] = ""
        self.cfg6 = CfgTest()
        self.cfg6.queue_list[0]["ext"] = "txt"
        self.cfg7 = CfgTest()
        self.cfg7.queue_list[0]["flatten"] = False
        self.cfg8 = CfgTest()
        self.cfg8.queue_list[0]["dtg"] = True
        self.cfg9 = CfgTest()
        self.cfg9.queue_list[0]["date"] = True
        self.cfg10 = CfgTest()
        self.cfg10.queue_list[0]["prename"] = ""
        self.cfg11 = CfgTest()
        self.cfg11.queue_list[0]["postname"] = ""
        self.cfg12 = CfgTest()
        self.cfg12.queue_list[0]["key"] = ""
        self.cfg12.queue_list[0]["postname"] = ""
        self.cfg12.queue_list[0]["prename"] = ""
        self.cfg13 = CfgTest()
        self.cfg13.queue_list[0]["routing_key"] = "NO_ROUTING_KEY"
        self.base_dir = "/BASE_DIR_PATH"
        self.method = MethodTest()
        self.body = {"Server": "SERVER_NAME.domain.name"}
        self.body2 = {"Non-Key": "Non-Value"}
        self.body3 = "This a string"
        self.rawbody = '{"Server": "SERVER_NAME.domain.name"}'
        self.rawbody2 = '{"Non-Key": "Non-Value"}'
        self.rawbody3 = '"This a string"'
        self.rawbody4 = '["This", "a", "string"]'
        self.rmq = "RabbitMQ Instance"

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_routing_key(self, mock_msg, mock_log):

        """Function:  test_no_routing_key

        Description:  Test with no routing key detected.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg13, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_default_name(self, mock_msg, mock_log):

        """Function:  test_default_name

        Description:  Test for default file name.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg12, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_postname(self, mock_msg, mock_log):

        """Function:  test_no_postname

        Description:  Test with no postname set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg11, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_postname(self, mock_msg, mock_log):

        """Function:  test_postname

        Description:  Test with postname set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_prename(self, mock_msg, mock_log):

        """Function:  test_no_prename

        Description:  Test with no prename set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg10, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_prename(self, mock_msg, mock_log):

        """Function:  test_prename

        Description:  Test with prename set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_date_true(self, mock_msg, mock_log):

        """Function:  test_date_true

        Description:  Test with date set to True.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg9, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_date_false(self, mock_msg, mock_log):

        """Function:  test_date_false

        Description:  Test with date set to False.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_dtg_true(self, mock_msg, mock_log):

        """Function:  test_dtg_true

        Description:  Test with dtg set to True.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg8, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_dtg_false(self, mock_msg, mock_log):

        """Function:  test_dtg_false

        Description:  Test with dtg set to False.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_flatten_false(self, mock_msg, mock_log):

        """Function:  test_flatten_false

        Description:  Test with flatten set to False.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg7, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_flatten_true(self, mock_msg, mock_log):

        """Function:  test_flatten_true

        Description:  Test with flatten set to True.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_ext_set(self, mock_msg, mock_log):

        """Function:  test_ext_set

        Description:  Test with ext set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg6, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_ext_set(self, mock_msg, mock_log):

        """Function:  test_no_ext_set

        Description:  Test with no ext set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_dict_key_set(self, mock_msg, mock_log):

        """Function:  test_no_dict_key_set

        Description:  Test with dict_key not set.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg5, self.method, self.rawbody))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_no_dict_key_pass(self, mock_msg, mock_log):

        """Function:  test_no_dict_key_pass

        Description:  Test with no dictionary key in dictionary.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg, self.method, self.rawbody2))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_any_pass(self, mock_msg, mock_log):

        """Function:  test_any_pass

        Description:  Test with any set for message type.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg4, self.method, self.rawbody3))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_str_pass(self, mock_msg, mock_log):

        """Function:  test_str_pass

        Description:  Test with string passed.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg3, self.method, self.rawbody3))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_list_pass(self, mock_msg, mock_log):

        """Function:  test_list_pass

        Description:  Test with list passed.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg2, self.method, self.rawbody4))

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

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
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

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    def test_convert_fails_type_pass(self, mock_msg, mock_log):

        """Function:  test_convert_fails_type_pass

        Description:  Test literal_eval fails for string, but passes for type.

        Arguments:

        """

        mock_msg.return_value = True
        mock_log.return_value = True

        self.assertFalse(rmq_2_sysmon.process_msg(
            self.rmq, mock_log, self.cfg3, self.method, self.body3))

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

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_2_sysmon.non_proc_msg")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    @mock.patch("rmq_2_sysmon.ast.literal_eval")
    def test_key_not_in_dict(self, mock_json, mock_log, mock_msg):

        """Function:  test_key_not_in_dict

        Description:  Test with no dictionary key found.

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


if __name__ == "__main__":
    unittest.main()

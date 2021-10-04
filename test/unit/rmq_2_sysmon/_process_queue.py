#!/usr/bin/python
# Classification (U)

"""Program:  _process_queue.py

    Description:  Unit testing of _process_queue in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/_process_queue.py

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
        test_key_not_in_dict
        test_create_json_fail
        test_create_json
        test_is_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.x_name = "rmq_2_isse_unit_test"
        self.queue = {
            "queue": "rmq_2_isse_unit_test",
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
            "flatten": True}

        self.queue2 = self.queue
        self.queue2["stype"] = "list"
        self.queue3 = self.queue
        self.queue3["stype"] = "str"
        self.queue4 = self.queue
        self.queue4["stype"] = "any"
        self.queue5 = self.queue
        self.queue5["key"] = ""
        self.queue6 = self.queue
        self.queue6["ext"] = "txt"
        self.queue7 = self.queue
        self.queue7["flatten"] = False
        self.queue8 = self.queue
        self.queue8["dtg"] = True
        self.queue9 = self.queue
        self.queue9["date"] = True
        self.queue10 = self.queue
        self.queue10["prename"] = ""
        self.queue11 = self.queue
        self.queue11["postname"] = ""
        self.queue12 = self.queue
        self.queue12["key"] = ""
        self.queue12["postname"] = ""
        self.queue12["prename"] = ""
        self.queue13 = self.queue
        self.queue13["routing_key"] = "NO_ROUTING_KEY"

        self.r_key = "Routing Key"

        self.body = {"Server": "SERVER_NAME.domain.name"}
        self.body2 = {"Non-Key": "Non-Value"}
        self.body3 = "This a string"
        self.body4 = ["This", "a", "list"]

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_default_name(self):

        """Function:  test_default_name

        Description:  Test for default file name.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue12, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_postname(self):

        """Function:  test_no_postname

        Description:  Test with no postname set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue11, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_postname(self):

        """Function:  test_postname

        Description:  Test with postname set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_prename(self):

        """Function:  test_no_prename

        Description:  Test with no prename set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue10, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_prename(self):

        """Function:  test_prename

        Description:  Test with prename set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_date_true(self):

        """Function:  test_date_true

        Description:  Test with date set to True.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue9, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_date_false(self):

        """Function:  test_date_false

        Description:  Test with date set to False.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_dtg_true(self):

        """Function:  test_dtg_true

        Description:  Test with dtg set to True.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue8, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_dtg_false(self):

        """Function:  test_dtg_false

        Description:  Test with dtg set to False.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_flatten_false(self):

        """Function:  test_flatten_false

        Description:  Test with flatten set to False.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue7, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_flatten_true(self):

        """Function:  test_flatten_true

        Description:  Test with flatten set to True.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_ext_set(self):

        """Function:  test_ext_set

        Description:  Test with ext set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue6, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_ext_set(self):

        """Function:  test_no_ext_set

        Description:  Test with no ext set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_dict_key_set(self):

        """Function:  test_no_dict_key_set

        Description:  Test with dict_key not set.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue5, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_dict_key_pass(self):

        """Function:  test_no_dict_key_pass

        Description:  Test with no dictionary key in dictionary.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body2, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_any_pass(self):

        """Function:  test_any_pass

        Description:  Test with any set for message type.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue4, self.body3, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_str_pass(self):

        """Function:  test_str_pass

        Description:  Test with string passed.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue3, self.body3, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_list_pass(self):

        """Function:  test_list_pass

        Description:  Test with list passed.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue2, self.body4, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_key_not_in_dict(self):

        """Function:  test_key_not_in_dict

        Description:  Test with no dictionary key found.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body2, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_create_json_fail(self):

        """Function:  test_create_json_fail

        Description:  Test if the body is unable to convert to JSON.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_create_json(self):

        """Function:  test_create_json

        Description:  Test if the body is converted to JSON.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))

    @mock.patch("rmq_2_sysmon.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_is_dict(self):

        """Function:  test_is_dict

        Description:  Test if the body is a dictionary.

        Arguments:

        """

        self.assertFalse(rmq_2_sysmon._process_queue(
            self.queue, self.body, self.r_key, self.x_name))


if __name__ == "__main__":
    unittest.main()

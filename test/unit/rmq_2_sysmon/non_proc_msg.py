#!/usr/bin/python
# Classification (U)

###############################################################################
#
# Program:      non_proc_msg.py
#
# Class Dependencies:
#               None
#
# Library Dependenices:
#               rmq_2_sysmon      => 0.0.1 or higher
#
###############################################################################

"""Program:  non_proc_msg.py

    Description:  Unit testing of non_proc_msg in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/non_proc_msg.py

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

# Version Information
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Initialize testing environment.
        test_to_empty_line -> Test for empty to line.
        test_to_line -> Test for valid to line.
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

                self.exchange = "test_exchange"
                self.queue_name = "test_queue"
                self.to_line = ""
                self.message_dir = "message_dir"

        self.CT = CfgTest()

    @mock.patch("rmq_2_sysmon.gen_class.Mail")
    @mock.patch("rmq_2_sysmon.gen_libs.write_file")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_empty_to_line(self, mock_log, mock_write, mock_mail):

        """Function:  test_empty_to_line

        Description:  Test non_proc_msg function with empty to line.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_write -> Mock Ref:  rmq_2_sysmon.gen_libs.write_file
            mock_mail -> Mock Ref:  rmq_2_sysmon.gen_class.Mail

        """

        mock_log.return_value = True
        mock_write.return_value = True
        mock_mail.send_mail.return_value = True

        self.assertFalse(rmq_2_sysmon.non_proc_msg(self.CT, mock_log, self.CT,
                                                   "Line", "Test_Subject"))

    @mock.patch("rmq_2_sysmon.gen_class.Mail")
    @mock.patch("rmq_2_sysmon.gen_libs.write_file")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_to_line(self, mock_log, mock_write, mock_mail):

        """Function:  test_to_line

        Description:  Test non_proc_msg function with valid to line.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_sysmon.gen_class.Logger
            mock_write -> Mock Ref:  rmq_2_sysmon.gen_libs.write_file
            mock_mail -> Mock Ref:  rmq_2_sysmon.gen_class.Mail

        """

        mock_log.return_value = True
        mock_write.return_value = True
        mock_mail.send_mail.return_value = True

        self.CT.to_line = "Test_Email@email.domain"

        self.assertFalse(rmq_2_sysmon.non_proc_msg(self.CT, mock_log, self.CT,
                                                   "Line", "Test_Subject"))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        self.CT = None


if __name__ == "__main__":
    unittest.main()

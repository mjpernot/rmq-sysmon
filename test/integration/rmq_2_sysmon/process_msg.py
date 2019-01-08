#!/usr/bin/python
# Classification (U)

###############################################################################
#
# Program:      process_msg.py
#
# Class Dependencies:
#               class.rabbitmq_class    => v0.3.0 or higher
#               lib.gen_class           => v2.4.0 or higher
#
# Library Dependenices:
#               rmq_2_sysmon            => v0.1.0 or higher
#               lib.gen_libs            => v2.4.0 or higher
#
###############################################################################

"""Program:  process_msg.py

    Description:  Integration testing of process_msg in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/process_msg.py

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
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
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
        test_non_proc_msg -> Test of non_proc_msg function call.
        test_body_dict_true -> Test of json.loads function.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:
            None

        """

        self.base_dir = "test/integration/rmq_2_sysmon"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")

        self.cfg = gen_libs.load_module("rabbitmq", self.config_path)

        log_path = os.path.join(self.test_path, self.cfg.log_dir)
        self.cfg.log_file = os.path.join(log_path, self.cfg.log_file)

        self.cfg.message_dir = os.path.join(self.test_path,
                                            self.cfg.message_dir)
        self.cfg.sysmon_dir = os.path.join(self.test_path, self.cfg.sysmon_dir)

        self.LOG = gen_class.Logger(self.cfg.log_file, self.cfg.log_file,
                                    "INFO",
                                    "%(asctime)s %(levelname)s %(message)s",
                                    "%Y-%m-%dT%H:%M:%SZ")
        self.RQ = rabbitmq_class.RabbitMQCon(self.cfg.user, self.cfg.passwd,
                                             self.cfg.host, self.cfg.port,
                                             self.cfg.exchange_name,
                                             self.cfg.exchange_type,
                                             self.cfg.queue_name,
                                             self.cfg.queue_name,
                                             self.cfg.x_durable,
                                             self.cfg.q_durable,
                                             self.cfg.auto_delete)

        self.method = "Method_Properties"
        self.body = '{"Server": "SERVER_NAME.domain.name"}'
        self.body2 = '["Server", "SERVER_NAME.domain.name"]'

        self.sysmon_file = os.path.join(self.cfg.sysmon_dir,
                                        "SERVER_NAME_pkgs.json")

        self.log_chk = "process_msg:  Processing body of message"
        self.non_proc_msg = "Non-dictionary format"

    @mock.patch("rmq_2_sysmon.gen_class.Mail")
    def test_non_proc_msg(self, mock_mail):

        """Function:  test_non_proc_msg

        Description:  Test of non_proc_msg function call.

        Arguments:
            mock_mail -> Mock Ref:  rmq_2_sysmon.gen_class.Mail

        """

        mock_mail.send_mail.return_value = True

        rmq_2_sysmon.process_msg(self.RQ, self.LOG, self.cfg, self.method,
                                 self.body2)

        self.LOG.log_close()

        if self.non_proc_msg in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    def test_body_dict_true(self):

        """Function:  test_body_dict_true

        Description:  Test of json.loads function.

        Arguments:
            None

        """

        rmq_2_sysmon.process_msg(self.RQ, self.LOG, self.cfg, self.method,
                                 self.body)

        self.LOG.log_close()

        if self.log_chk in open(self.cfg.log_file).read() and \
           os.path.isfile(self.sysmon_file):
            status = True

        else:
            status = False

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:
            None

        """

        os.remove(self.cfg.log_file)

        if os.path.isfile(self.sysmon_file):
            os.remove(self.sysmon_file)

        for f_name in os.listdir(self.cfg.message_dir):

            if ".gitignore" not in f_name:
                os.remove(os.path.join(self.cfg.message_dir, f_name))


if __name__ == "__main__":
    unittest.main()

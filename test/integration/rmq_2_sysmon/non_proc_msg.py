#!/usr/bin/python
# Classification (U)

"""Program:  non_proc_msg.py

    Description:  Integration testing of non_proc_msg in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/non_proc_msg.py

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
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_write_file
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
        self.cfg.message_dir = os.path.join(self.test_path,
                                            self.cfg.message_dir)
        self.log = gen_class.Logger(
            self.cfg.log_file, self.cfg.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        self.rmq = rabbitmq_class.RabbitMQCon(
            self.cfg.user, self.cfg.japd, self.cfg.host, self.cfg.port,
            exchange_name=self.cfg.exchange_name,
            exchange_type=self.cfg.exchange_type,
            queue_name=self.cfg.queue_list[0]["queue"],
            routing_key=self.cfg.queue_list[0]["routing_key"],
            x_durable=self.cfg.x_durable, q_durable=self.cfg.q_durable,
            auto_delete=self.cfg.auto_delete, heartbeat=self.cfg.heartbeat,
            host_list=self.cfg.host_list)
        self.line = "Test_Me_File"
        self.subj = "Test_Me"
        self.test_file = None

    @mock.patch("rmq_2_sysmon.gen_class.Mail")
    def test_write_file(self, mock_mail):

        """Function:  test_write_file

        Description:  Test of gen_libs.write_file call.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        rmq_2_sysmon.non_proc_msg(self.rmq, self.log, self.cfg, self.line,
                                  self.subj, self.rmq.routing_key)
        self.log.log_close()

        self.test_file = gen_libs.dir_file_match(self.cfg.message_dir,
                                                 self.rmq.exchange)[0]

        self.assertTrue(self.line in open(os.path.join(self.cfg.message_dir,
                                                       self.test_file)).read())

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.log_file)
        os.remove(os.path.join(self.cfg.message_dir, self.test_file))
        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()

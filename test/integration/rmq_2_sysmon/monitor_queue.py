# Classification (U)

"""Program:  monitor_queue.py

    Description:  Integration testing of monitor_queue in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/monitor_queue.py

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
import rmq_cleanup                              # pylint:disable=E0401,C0413
import rmq_2_sysmon                             # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_rabbitmq_class
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
        self.connect_true = "Connected to RabbitMQ node"

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon.consume")
    def test_rabbitmq_class(self, mock_consume):

        """Function:  test_rabbitmq_class

        Description:  Test of rabbitmq_class.RabbitMQCon class and connection.

        Arguments:
            mock_consume -> Mock Ref:  rmq_2_sysmon.rabbitmq_class.RabbitMQCon

        """

        mock_consume.return_value = "RabbitMQ_Tag"
        rmq_2_sysmon.monitor_queue(self.cfg, self.log)
        self.log.log_close()

        self.assertTrue(
            self.connect_true in open(                  # pylint:disable=R1732
                self.cfg.log_file, encoding="UTF-8").read())

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.log_file)
        rmq_cleanup.rmq_cleanup(self.cfg, self.cfg.queue_list[0]["queue"],
                                True)


if __name__ == "__main__":
    unittest.main()

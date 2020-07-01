#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Integration testing of main in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/main.py

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
import rmq_cleanup
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_main_program_args -> Test passing arguments via program call.
        tearDown -> Clean up of testing environment.

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
        self.cfg.queue_list[0]["directory"] = os.path.join(
            self.test_path, self.cfg.queue_list[0]["directory"])
        self.connect_true = "Connected to RabbitMQ node"
        self.argv_list = [os.path.join(self.base_dir, "main.py"), "-M", "-c",
                          "rabbitmq", "-d", "config"]

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon.consume")
    def test_main_program_args(self, mock_consume, mock_cfg, mock_base):

        """Function:  test_main_program_args

        Description:  Test passing arguments via program call.

        Arguments:

        """

        mock_consume.return_value = "RabbitMQ_Tag"
        mock_cfg.return_value = self.cfg
        mock_base.return_value = self.test_path
        rmq_2_sysmon.main(argv_list=self.argv_list)

        self.assertTrue(self.connect_true in open(self.cfg.log_file).read())

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

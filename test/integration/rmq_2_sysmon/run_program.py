# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/run_program.py

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
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_args_keys
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args = {}

    def get_args_keys(self):

        """Method:  get_args_keys

        Description:  Method stub holder for gen_class.ArgParser.get_args_keys.

        Arguments:

        """

        return list(self.args_array.keys())

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_run_program
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
        self.cfg.queue_list[0]["directory"] = os.path.join(
            self.test_path, self.cfg.queue_list[0]["directory"])
        self.connect_true = "Connected to RabbitMQ node"
        self.args = ArgParser()
        self.args.args_array = {"-M": True, "-c": "rabbitmq", "-d": "config"}
        self.func_names = {"-M": rmq_2_sysmon.monitor_queue}

    @mock.patch("rmq_2_sysmon.gen_libs.get_base_dir")
    @mock.patch("rmq_2_sysmon.gen_libs.load_module")
    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon.consume")
    def test_run_program(self, mock_consume, mock_cfg, mock_base):

        """Function:  test_run_program

        Description:  Test of test_run_program function.

        Arguments:

        """

        mock_consume.return_value = "RabbitMQ_Tag"
        mock_cfg.return_value = self.cfg
        mock_base.return_value = self.test_path
        rmq_2_sysmon.run_program(self.args, self.func_names)

        self.assertIn(
            self.connect_true, open(                    # pylint:disable=R1732
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

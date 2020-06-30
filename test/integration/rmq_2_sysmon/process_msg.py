#!/usr/bin/python
# Classification (U)

"""Program:  process_msg.py

    Description:  Integration testing of process_msg in rmq_2_sysmon.py.

    Usage:
        test/integration/rmq_2_sysmon/process_msg.py

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
        setUp -> Initialize testing environment.
        test_non_proc_msg -> Test of non_proc_msg function call.
        test_body_dict_true -> Test of json.loads function.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

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

                self.routing_key = "intr-test"

        self.method = MethodTest()
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
        self.log = gen_class.Logger(self.cfg.log_file, self.cfg.log_file,
                                    "INFO",
                                    "%(asctime)s %(levelname)s %(message)s",
                                    "%Y-%m-%dT%H:%M:%SZ")
        self.rmq = rabbitmq_class.RabbitMQCon(
            self.cfg.user, self.cfg.passwd, self.cfg.host, self.cfg.port,
            exchange_name=self.cfg.exchange_name,
            exchange_type=self.cfg.exchange_type,
            queue_name=self.cfg.queue_list[0]["queue"],
            routing_key=self.cfg.queue_list[0]["routing_key"],
            x_durable=self.cfg.x_durable, q_durable=self.cfg.q_durable,
            auto_delete=self.cfg.auto_delete)
        self.body = '{"Server": "SERVER_NAME.domain.name"}'
        self.body2 = '["Server", "SERVER_NAME.domain.name"]'
        self.sysmon_file = os.path.join(self.cfg.queue_list[0]["directory"],
                                        "SERVER_NAME_pkgs.json")
        self.log_chk = "process_msg:  Processing message body from Routing Key"
        self.non_proc_msg = "Incorrect type"

    @mock.patch("rmq_2_sysmon.gen_class.Mail")
    def test_non_proc_msg(self, mock_mail):

        """Function:  test_non_proc_msg

        Description:  Test of non_proc_msg function call.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        rmq_2_sysmon.process_msg(self.rmq, self.log, self.cfg, self.method,
                                 self.body2)
        self.log.log_close()

        self.assertTrue(self.non_proc_msg in open(self.cfg.log_file).read())

    def test_body_dict_true(self):

        """Function:  test_body_dict_true

        Description:  Test of json.loads function.

        Arguments:

        """

        rmq_2_sysmon.process_msg(self.rmq, self.log, self.cfg, self.method,
                                 self.body)
        self.log.log_close()

        self.assertTrue(self.log_chk in open(self.cfg.log_file).read() and \
                        os.path.isfile(self.sysmon_file))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.log_file)

        if os.path.isfile(self.sysmon_file):
            os.remove(self.sysmon_file)

        for f_name in os.listdir(self.cfg.message_dir):

            if f_name not in [".gitignore", ".gitkeep"]:
                os.remove(os.path.join(self.cfg.message_dir, f_name))


if __name__ == "__main__":
    unittest.main()

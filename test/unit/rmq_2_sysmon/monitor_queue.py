#!/usr/bin/python
# Classification (U)

"""Program:  monitor_queue.py

    Description:  Unit testing of monitor_queue in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/monitor_queue.py

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
        test_two_queue_partial2 -> Test with two queues w/ first queue failure.
        test_two_queue_partial -> Test with two queues with one queue failure.
        test_two_queue_fail -> Test with two queues fails to initialize.
        test_two_queue_success -> Test with two queues initialized & monitored.
        test_one_queue_fail -> Test with one queue fails to initialize.
        test_one_queue_success -> Test with one queue initialized & monitored.
        test_false_and_data_msg -> Test with status is False and error message.
        test_false_and_false -> Test status is False and channel is False.
        test_true_and_false -> Test status is True and channel is False.
        test_false_and_true -> Test status is False and channel is True.
        test_true_and_true -> Test status is True and channel is True.
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

                self.user = "USER"
                self.passwd = ""
                self.host = "SERVER_NAME"
                self.port = 5672
                self.exchange_name = "EXCHANGE_NAME"
                self.exchange_type = "EXCHANGE_TYPE"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = False
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

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_two_queue_partial2(self, mock_log, mock_rq):

        """Function:  test_two_queue_partial2

        Description:  Test with two queues with first queue failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.side_effect = [(False, "Error"), (True, "")]
        mock_rq.channel.is_open.side_effect = [False, True]
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_two_queue_partial(self, mock_log, mock_rq):

        """Function:  test_two_queue_partial

        Description:  Test with two queues with one queue failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.side_effect = [(True, ""), (False, "Error")]
        mock_rq.channel.is_open.side_effect = [True, False]
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_one_queue_fail(self, mock_log, mock_rq):

        """Function:  test_one_queue_fail

        Description:  Test with one queue fails to initialize.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (False, "Error Message")
        mock_rq.channel.is_open = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_one_queue_success(self, mock_log, mock_rq):

        """Function:  test_one_queue_success

        Description:  Test with one queue initialized and monitored.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (True, "")
        mock_rq.channel.is_open = True
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_data_msg(self, mock_log, mock_rq):

        """Function:  test_false_and_data_msg

        Description:  Test process_msg function with status is False and error
            message.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (False, "Error_Message")

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_false(self, mock_log, mock_rq):

        """Function:  test_false_and_false

        Description:  Test process_msg function with status is False and
            channel is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (False, "Error_Message")
        mock_rq.channel.is_open = False

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_true_and_false(self, mock_log, mock_rq):

        """Function:  test_true_and_false

        Description:  Test process_msg function with status is True and
            channel is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (True, "Error_Message")
        mock_rq.channel.is_open = False

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_true(self, mock_log, mock_rq):

        """Function:  test_false_and_true

        Description:  Test process_msg function with status is False and
            channel is True.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (False, "Error_Message")
        mock_rq.channel.is_open = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.RabbitMQCon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_true_and_true(self, mock_log, mock_rq):

        """Function:  test_true_and_true

        Description:  Test process_msg function with status is True and
            channel is True.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.RabbitMQCon
        mock_rq.create_connection.return_value = (True, "Error_Message")
        mock_rq.channel.is_open = True
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.cfg = None


if __name__ == "__main__":
    unittest.main()

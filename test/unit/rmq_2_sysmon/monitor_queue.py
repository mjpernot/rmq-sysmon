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


class CfgTest(object):

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.user = "USER"
        self.japd = ""
        self.host = "SERVER_NAME"
        self.host_list = []
        self.port = 5672
        self.exchange_name = "EXCHANGE_NAME"
        self.exchange_type = "EXCHANGE_TYPE"
        self.x_durable = True
        self.q_durable = True
        self.auto_delete = False
        self.heartbeat = 60
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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_two_queue_partial2
        test_two_queue_partial
        test_two_queue_fail
        test_two_queue_success
        test_one_queue_fail
        test_one_queue_success
        test_false_and_data_msg
        test_false_and_false
        test_true_and_false
        test_false_and_true
        test_true_and_true
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_two_queue_partial2(self, mock_log, mock_rq):

        """Function:  test_two_queue_partial2

        Description:  Test with two queues with first queue failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.side_effect = [(False, "Error"), (True, "")]
        mock_rq.channel.is_open.side_effect = [False, True]
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_two_queue_partial(self, mock_log, mock_rq):

        """Function:  test_two_queue_partial

        Description:  Test with two queues with one queue failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.side_effect = [(True, ""), (False, "Error")]
        mock_rq.channel.is_open.side_effect = [True, False]
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_one_queue_fail(self, mock_log, mock_rq):

        """Function:  test_one_queue_fail

        Description:  Test with one queue fails to initialize.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (False, "Error Message")
        mock_rq.channel.is_open = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_one_queue_success(self, mock_log, mock_rq):

        """Function:  test_one_queue_success

        Description:  Test with one queue initialized and monitored.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (True, "")
        mock_rq.channel.is_open = True
        mock_rq.consume.return_value = "RabbitMQ_Tag"
        mock_rq.start_loop.return_value = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_data_msg(self, mock_log, mock_rq):

        """Function:  test_false_and_data_msg

        Description:  Test process_msg function with status is False and error
            message.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (False, "Error_Message")

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_false(self, mock_log, mock_rq):

        """Function:  test_false_and_false

        Description:  Test process_msg function with status is False and
            channel is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (False, "Error_Message")
        mock_rq.channel.is_open = False

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_true_and_false(self, mock_log, mock_rq):

        """Function:  test_true_and_false

        Description:  Test process_msg function with status is True and
            channel is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (True, "Error_Message")
        mock_rq.channel.is_open = False

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_false_and_true(self, mock_log, mock_rq):

        """Function:  test_false_and_true

        Description:  Test process_msg function with status is False and
            channel is True.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
        mock_rq.create_connection.return_value = (False, "Error_Message")
        mock_rq.channel.is_open = True

        self.assertFalse(rmq_2_sysmon.monitor_queue(self.cfg, mock_log))

    @mock.patch("rmq_2_sysmon.rabbitmq_class.create_rmqcon")
    @mock.patch("rmq_2_sysmon.gen_class.Logger")
    def test_true_and_true(self, mock_log, mock_rq):

        """Function:  test_true_and_true

        Description:  Test process_msg function with status is True and
            channel is True.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = rmq_2_sysmon.rabbitmq_class.create_rmqcon
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

#!/usr/bin/python
# Classification (U)

"""Program:  rmq_cleanup.py

    Description:  Cleanup of RabbitMQ exchange and queues.

    Usage:
        test/blackbox/rmq_2_sysmon/rmq_cleanup.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys

# Third-party
import pika

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def rmq_cleanup(cfg, queue_name, drop_exch=False):

    """Function:  rmq_cleanup

    Description:  Cleanup RabbitMQ exchanges and queues.

    Arguments:
        (input) cfg -> RabbitMQ configuration module handler.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch -> True|False - Drop the exchange.

    """

    rmq = rabbitmq_class.RabbitMQPub(
        cfg.user, cfg.passwd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=queue_name, routing_key=queue_name,
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)

    if isinstance(rmq, rabbitmq_class.RabbitMQPub):
        connect_status, err_msg = rmq.connect()

        if isinstance(rmq.connection,
                      pika.adapters.blocking_connection.BlockingConnection) \
                and rmq.connection._impl.connection_state > 0 \
                and connect_status:

            rmq.open_channel()

            if rmq.channel.is_open:
                rmq.setup_exchange()

                try:
                    rmq.channel.exchange_declare(exchange=rmq.exchange,
                                                 passive=True)
                    rmq.create_queue()
                    _cleanup(rmq, connect_status, drop_exch)

                except pika.exceptions.ChannelClosed as msg:
                    print("\tWarning:  Unable to find an exchange")
                    print("Error Msg: %s" % msg)

            else:
                print("\tFailure:  Unable to open channel")
                print("\tChannel: %s" % rmq.channel)

        else:
            print("\tFailure:  Unable to open connection")
            print("\tConnection: %s" % rmq.connection)
            print("\tError Msg: %s" % err_msg)

    else:
        print("\tFailure:  Unable to initialize")
        print("\tClass: %s" % rabbitmq_class.RabbitMQPub)


def _cleanup(rmq, connect_status, drop_exch):

    """Function:  _cleanup

    Description:  Private function for rmq_cleanup.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch -> True|False - Drop the exchange.

    """

    try:
        rmq.channel.queue_declare(queue=rmq.queue_name, passive=True)
        rmq.clear_queue()
        rmq.drop_queue()

        if drop_exch:
            rmq.drop_exchange()

        rmq.close_channel()

        if rmq.channel.is_closed:
            if connect_status and rmq.connection._impl.connection_state > 0:
                rmq.close()

                if rmq.connection._impl.connection_state != 0:
                    print("\tFailed to close connection")
                    print("\tConnection: %s" % rmq.connection)
                    print("\tConnection State: %s" %
                          rmq.connection._impl.connection_state)

            else:
                print("\tConnection not opened")

        else:
            print("\tFailure:  Channel did not close")
            print("\tChannel: %s" % rmq.channel)

    except pika.exceptions.ChannelClosed as msg:
        print("\tWarning:  Unable to locate queue")
        print("Error Msg: %s" % msg)


def main():

    """Function:  main

    Description:  Control the cleanup of RabbitMQ exchange and queues.

    Variables:
        base_dir -> Path directory to blackbox testing.
        test_path -> Full path directory to blackbox testing.
        config_path -> Path directory to configuration directory.
        cfg -> Configuration settings module for the program.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    cfg = gen_libs.load_module("rabbitmq", config_path)
    rmq_cleanup(cfg, cfg.queue_list[0]["queue"], True)


if __name__ == "__main__":
    sys.exit(main())

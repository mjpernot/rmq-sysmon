#!/usr/bin/python
# Classification (U)

###############################################################################
#
# Program:      rmq_cleanup.py
#
# Class Dependencies:
#               class.rabbitmq_class    => v0.3.0 or higher
#
# Library Dependenices:
#               lib.gen_libs            => v2.4.0 or higher
#
###############################################################################

"""Program:  rmq_cleanup.py

    Description:  Cleanup of RabbitMQ exchange and queues.

    Usage:
        test/integration/rmq_2_sysmon/rmq_cleanup.py

    Arguments:
        None

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

# Version Information
__version__ = version.__version__


def rmq_cleanup(cfg, queue_name, drop_exch=False):

    """Function:  rmq_cleanup

    Description:  Cleanup RabbitMQ exchanges and queues.

    Arguments:
        (input) cfg -> RabbitMQ configuration module handler.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch -> True|False - Drop the exchange.

    """

    RQ = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    queue_name, queue_name, cfg.x_durable,
                                    cfg.q_durable, cfg.auto_delete)

    if isinstance(RQ, rabbitmq_class.RabbitMQPub):
        connect_status, err_msg = RQ.connect()

        if isinstance(RQ.connection,
                      pika.adapters.blocking_connection.BlockingConnection) \
                and RQ.connection._impl.connection_state > 0 \
                and connect_status:

            RQ.open_channel()

            if RQ.channel.is_open:
                RQ.setup_exchange()

                try:
                    RQ.channel.exchange_declare(exchange=RQ.exchange,
                                                passive=True)

                    RQ.create_queue()

                    try:
                        RQ.channel.queue_declare(queue=RQ.queue_name,
                                                 passive=True)

                        RQ.clear_queue()
                        RQ.drop_queue()

                        if drop_exch:
                            RQ.drop_exchange()

                        RQ.close_channel()

                        if RQ.channel.is_closed:

                            if connect_status \
                                    and RQ.connection._impl.connection_state \
                                    > 0:

                                RQ.close()

                                if RQ.connection._impl.connection_state == 0:
                                    pass

                                else:
                                    print("\tFailed to close connection")
                                    print("\tConnection: %s" % RQ.connection)
                                    print("\tConnection State: %s" %
                                          RQ.connection._impl.connection_state)

                            else:
                                print("\tConnection not opened")

                        else:
                            print("\tFailure:  Channel did not close")
                            print("\tChannel: %s" % RQ.channel)

                    except pika.exceptions.ChannelClosed as msg:
                        print("\tWarning:  Unable to locate queue")
                        print("Error Msg: %s" % msg)

                except pika.exceptions.ChannelClosed as msg:
                    print("\tWarning:  Unable to find an exchange")
                    print("Error Msg: %s" % msg)

            else:
                print("\tFailure:  Unable to open channel")
                print("\tChannel: %s" % RQ.channel)

        else:
            print("\tFailure:  Unable to open connection")
            print("\tConnection: %s" % RQ.connection)
            print("\tError Msg: %s" % err_msg)

    else:
        print("\tFailure:  Unable to initialize")
        print("\tClass: %s" % rabbitmq_class.RabbitMQPub)


def main():

    """Function:  main

    Description:  Control the cleanup of RabbitMQ exchange and queues.

    Variables:
        None

    Arguments:
        None

    """

    base_dir = "test/integration/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")

    cfg = gen_libs.load_module("rabbitmq", config_path)

    print("\nRabbitMQ cleanup...")
    rmq_cleanup(cfg, cfg.queue_name, True)


if __name__ == "__main__":
    sys.exit(main())

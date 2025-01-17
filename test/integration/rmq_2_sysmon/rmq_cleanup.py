# Classification (U)

"""Program:  rmq_cleanup.py

    Description:  Cleanup of RabbitMQ exchange and queues.

    Usage:
        test/integration/rmq_2_sysmon/rmq_cleanup.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import pika

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rmqcls  # pylint:disable=E0401,C0413,R0402
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def rmq_cleanup(cfg, queue_name, drop_exch=False):

    """Function:  rmq_cleanup

    Description:  Cleanup RabbitMQ exchanges and queues.

    Arguments:
        (input) cfg -> RabbitMQ configuration module handler.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch -> True|False - Drop the exchange.

    """

    rmq = rmqcls.create_rmqpub(cfg, queue_name, queue_name)

    if isinstance(rmq, rmqcls.RabbitMQPub):
        connect_status, err_msg = rmq.connect()

        state = rmq.connection._impl.connection_state   # pylint:disable=W0212
        if isinstance(rmq.connection,
                      pika.adapters.blocking_connection.BlockingConnection) \
                and state > 0 and connect_status:

            rmq.open_channel()

            if rmq.channel.is_open:
                rmq.setup_exchange()

                try:
                    rmq.channel.exchange_declare(
                        exchange=rmq.exchange, passive=True)
                    rmq.create_queue()
                    cleanup(rmq, connect_status, drop_exch)

                except pika.exceptions.ChannelClosed as msg:
                    print("\tWarning:  Unable to find an exchange")
                    print(f"Error Msg: {msg}")

            else:
                print("\tFailure:  Unable to open channel")
                print(f"\tChannel: {rmq.channel}")

        else:
            print("\tFailure:  Unable to open connection")
            print(f"\tConnection: {rmq.connection}")
            print(f"\tError Msg: {err_msg}")

    else:
        print("\tFailure:  Unable to initialize")
        print(f"\tClass: {rmqcls.RabbitMQPub}")


def cleanup(rmq, connect_status, drop_exch):

    """Function:  cleanup

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
            sta = rmq.connection._impl.connection_state  # pylint:disable=W0212
            if connect_status and sta > 0:
                rmq.close()

                if sta != 0:
                    print("\tFailed to close connection")
                    print(f"\tConnection: {rmq.connection}")
                    print(f"\tConnection State: {sta}")

            else:
                print("\tConnection not opened")

        else:
            print("\tFailure:  Channel did not close")
            print(f"\tChannel: {rmq.channel}")

    except pika.exceptions.ChannelClosed as msg:
        print("\tWarning:  Unable to locate queue")
        print(f"Error Msg: {msg}")


def main():

    """Function:  main

    Description:  Control the cleanup of RabbitMQ exchange and queues.

    Variables:

    Arguments:

    """

    base_dir = "test/integration/rmq_2_sysmon"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    cfg = gen_libs.load_module("rabbitmq", config_path)
    print("\nRabbitMQ cleanup...")
    rmq_cleanup(cfg, cfg.queue_name, True)


if __name__ == "__main__":
    sys.exit(main())

# Classification (U)

"""Program:  blackbox_libs.py

    Description:  Blackbox libraries for the test testing of rmq_2_sysmon.py
        program.

    Usage:
        test/blackbox/rmq_2_sysmon/blackbox_libs.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import json

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rmq_cls  # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def create_rq_pub(cfg):

    """Function:  create_rq_pub

    Description:  Create a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (output) rmq -> RabbitMQ Publisher instance

    """

    rmq = rmq_cls.RabbitMQPub(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        return rmq

    print("Error:  Failed to connect to RabbitMQ as Publisher.")
    print(f"Error Message: {err_msg}")
    return None


def file_test(f_name):

    """Function:  file_test

    Description:  Test to see if the file exists and in the correct format.

    Arguments:
        (input) f_name ->  Full path and file name of sysmon test file.
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message.

    """

    status = True
    err_msg = None

    if os.path.isfile(f_name):
        with open(f_name, mode="r", encoding="UTF-8") as f_hldr:
            body = f_hldr.read()

        data = json.loads(body)

        if not isinstance(data, dict):
            err_msg = f"\tError:  {f_name} is not in dictionary format."
            status = False

    else:
        err_msg = f"\tError:  {f_name} is not present"
        status = False

    return status, err_msg


def publish_msg(rmq, f_name):

    """Function:  publish_msg

    Description:  Publish a message to RabbitMQ.

    Arguments:
        (input) rmq -> RabbitMQ Publisher instance
        (input) f_name ->  Full path and file name of test file.
        (output) status -> True|False - Status of publish.
        (output) err_msg -> Error message.

    """

    status = True
    err_msg = None

    with open(f_name, mode="r", encoding="UTF-8") as f_hldr:
        body = f_hldr.read()

    if not rmq.publish_msg(body):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    return status, err_msg

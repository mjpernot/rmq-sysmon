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
import time

# Third-party
import json

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def create_rq_pub(cfg, **kwargs):

    """Function:  create_rq_pub

    Description:  Create a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (output) rq -> RabbitMQ Publisher instance

    """

    rq = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    cfg.queue_name, cfg.queue_name,
                                    cfg.x_durable, cfg.q_durable,
                                    cfg.auto_delete)
    connect_status, err_msg = rq.create_connection()

    if connect_status and rq.channel.is_open:
        return rq

    else:
        print("Error:  Failed to connect to RabbitMQ as Publisher.")
        print("Error Message: %s" % (err_msg))
        return None


def file_test(f_name, **kwargs):

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
        with open(f_name, "r") as f_hldr:
            body = f_hldr.read()

        data = json.loads(body)

        if not isinstance(data, dict):
            err_msg = "\tError:  %s is not in dictionary format." % (f_name)
            status = False

    else:
        err_msg = "\tError:  %s is not present" % (f_name)
        status = False

    return status, err_msg


def publish_msg(rq, f_name, **kwargs):

    """Function:  publish_msg

    Description:  Publish a message to RabbitMQ.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) f_name ->  Full path and file name of test file.
        (output) status -> True|False - Status of publish.
        (output) err_msg -> Error message.

    """

    status = True
    err_msg = None

    with open(f_name, "r") as f_hldr:
        body = f_hldr.read()

    if not rq.publish_msg(body):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    return status, err_msg

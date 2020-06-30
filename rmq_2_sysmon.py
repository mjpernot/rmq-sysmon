#!/usr/bin/python
# Classification (U)

"""Program:  rmq_2_sysmon.py

    Description:  Processes administration monitoring emails in RabbitMQ.  The
        program will process a number of different data types in the report,
        and will be able to save the report to a specified directory.

    Usage:
        rmq_2_sysmon.py -c config_file -d dir_path {-M}
            [-v | -h]

    Arguments:
        -c config_file => RabbitMQ configuration file.
            Required argument.
        -d dir_path => Directory path for option '-c'.
            Required argument.
        -M => Monitor and process messages from a RabbitMQ queue.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.

    Notes:
        The option to monitor the RabbitMQ is setup to run in an infinite loop
        and can only be killed with a CTRL-C on the command line, stopping the
        daemon, or shutting down of the service.

        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            # RabbitMQ Configuration file
            user = "USER"
            passwd = "PASSWORD"
            host = "HOSTNAME"
            # RabbitMQ Exchange name being monitored.
            exchange_name = "EXCHANGE_NAME"
            # Email address(es) to send non-processed messages to or None.
            # None state no emails are required to be sent.
            to_line = "EMAIL_ADDRESS"
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Queues automatically delete message after processing: True|False
            auto_delete = False
            # Archive directory name for non-processed messages.
            message_dir = "DIRECTORY_PATH/message_dir"
            # Directory name for log files.
            log_dir = "DIRECTORY_PATH/logs"
            # File name to program log.
            log_file = "rmq_2_sysmon.log"
            # List of queues to monitor.
            # Make a copy of the dictionary for each combination of a queue
                name and routing key.
            # -> queue:  "QUEUE_NAME" - Name of queue to monitor.
            # -> routing_key:  "ROUTING_KEY" - Name of the routing key for the
                queue.
            # -> directory:  "/DIR_PATH" - Directory path to where a report
                will be written to.
            # -> prename:  "NAME" - Static pre-file name string.
            # -> postname:  "NAME" - Static post-file name string.
            # -> key:  "DICT_KEY" - Is the name of a key in a dictionary.
            # -> mode:  "a"|"w" - Write mode to the file: write or append to a
                file.
            # -> ext:  "NAME" - Extension name to the file name.
            # -> dtg:  True|False - Add a date and time group to the file name.
            # -> date:  True|False - Add a date to the file name.
            # -> stype:  "any"|"dict"|"list"|"str" - Format of the messages
                that are allowed in the message.
            # -> flatten:  True|False - Flattens a dictionary format.
            queue_list = [
                    {"queue": "QUEUE_NAME",
                     "routing_key": "ROUTING_KEY",
                     "directory": "DIR_PATH",
                     "prename": "",
                     "postname": "",
                     "key": "",
                     "mode": "a",
                     "ext": "",
                     "dtg": False,
                     "date":  False,
                     "stype": "any",
                     "flatten": True
                    },
                    {"queue": "QUEUE_NAME",
                     "routing_key": "ROUTING_KEY",
                     "directory": "DIR_PATH",
                     "prename": "",
                     "postname": "",
                     "key": "",
                     "mode": "a",
                     "ext": "",
                     "dtg": False,
                     "date":  False,
                     "stype": "any",
                     "flatten": True
                    }
                ]

    Example:
        Command Line:
            rmq_2_sysmon.py -c rabbitmq -d config -M

        Daemon:
            daemon_rmq_2_sysmon.py -a start -c rabbitmq -d /path/config -M

        Service:
            service rmq_2_sysmon start

"""

# Libraries and Global Variables

# Standard
import sys
import os
import socket
import getpass
import datetime

# Third-party
import ast
import json

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def validate_create_settings(cfg, **kwargs):

    """Function:  validate_create_settings

    Description:  Validate the configuration settings and creation of certain
        settings.

    Arguments:
        (input) cfg -> Configuration module name.
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validation/creation.
        (output) err_msg -> Error message from checks.

    """

    err_msg = ""
    status_flag = True
    base_dir = gen_libs.get_base_dir(__file__)

    if not os.path.isabs(cfg.message_dir):
        cfg.message_dir = os.path.join(base_dir, cfg.message_dir)

    if not os.path.isabs(cfg.log_dir):
        cfg.log_dir = os.path.join(base_dir, cfg.log_dir)

    status, msg = gen_libs.chk_crt_dir(cfg.message_dir, write=True, read=True,
                                       no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    status, msg = gen_libs.chk_crt_dir(cfg.log_dir, write=True, read=True,
                                       no_print=True)

    if status:
        base_name, ext_name = os.path.splitext(cfg.log_file)
        log_name = base_name + "_" + cfg.exchange_name + ext_name
        cfg.log_file = os.path.join(cfg.log_dir, log_name)

    else:
        err_msg = err_msg + msg
        status_flag = False

    for queue in cfg.queue_list:
        status, msg = gen_libs.chk_crt_dir(queue["directory"], write=True,
                                           read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    return cfg, status_flag, err_msg


def non_proc_msg(rmq, log, cfg, data, subj, r_key, **kwargs):

    """Function:  non_proc_msg

    Description:  Process non-processed messages.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) data -> Body of message that was not processed.
        (input) subj -> Email subject line.
        (input) r_key -> Routing key for message.

    """

    log.log_info(
        "non_proc_msg:  Processing failed message from Routing Key: %s" %
        (r_key))
    frm_line = getpass.getuser() + "@" + socket.gethostname()
    rdtg = datetime.datetime.now()
    msecs = str(rdtg.microsecond / 1000)
    dtg = datetime.datetime.strftime(rdtg, "%Y-%m-%d_%H:%M:%S") + "." + msecs
    f_name = rmq.exchange + "_" + r_key + "_" + dtg + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    subj = "rmq_2_sysmon: " + subj

    if cfg.to_line:
        log.log_info("Sending email to: %s..." % (cfg.to_line))
        email = gen_class.Mail(cfg.to_line, subj, frm_line)
        email.add_2_msg(data)
        email.send_mail()

    else:
        log.log_warn("No email being sent as TO line is empty.")

    log.log_err("RabbitMQ message was not processed due to: %s" % (subj))
    log.log_info("Saving message to: %s" % (f_path))
    gen_libs.write_file(f_path, data="Exchange: %s, Routing Key: %s"
                        % (rmq.exchange, r_key))
    gen_libs.write_file(f_path, data=data)


def process_msg(rmq, log, cfg, method, body, **kwargs):

    """Function:  process_msg

    Description:  Process message from RabbitMQ queue.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) method -> Delivery properties.
        (input) body -> Message body.

    """

    r_key = method.routing_key
    queue = None
    log.log_info(
        "process_msg:  Processing message body from Routing Key: %s" % (r_key))

    for item in cfg.queue_list:

        if item["routing_key"] == r_key:
            queue = item
            break

    if queue:

        _convert_data(rmq, log, cfg, queue, body, r_key)

    else:
        non_proc_msg(rmq, log, cfg, body, "No queue detected", r_key)


def _convert_data(rmq, log, cfg, queue, body, r_key, **kwargs):

    """Function:  _process_queue

    Description:  Private function to process message queue.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) queue -> RabbitMQ queue.
        (input) body -> Message body.
        (input) r_key -> Routing key.

    """

    try:
        data = ast.literal_eval(body)

        if queue["stype"] == "any" \
           or (queue["stype"] == "dict" and isinstance(data, dict)) \
           or (queue["stype"] == "list" and isinstance(data, list)) \
           or (queue["stype"] == "str" and isinstance(data, str)):

            _process_queue(queue, data, r_key, cfg.exchange_name)

        else:
            msg = "Incorrect type detected: %s" % (type(data))
            non_proc_msg(rmq, log, cfg, body, msg, r_key)

    except (SyntaxError) as err:

        if isinstance(body, str) and (queue["stype"] == "any" or
                                      queue["stype"] == "str"):

            _process_queue(queue, body, r_key, cfg.exchange_name)

        else:
            non_proc_msg(rmq, log, cfg, body, str(err), r_key)

    except (ValueError) as err:
        non_proc_msg(rmq, log, cfg, body, str(err), r_key)


def _process_queue(queue, data, r_key, x_name, **kwargs):

    """Function:  _process_queue

    Description:  Private function to process message queue.

    Arguments:
        (input) queue -> RabbitMQ queue.
        (input) data -> Converted message body.
        (input) r_key -> Routing key.
        (input) x_name -> Exchange name.

    """

    k_name = ""
    ext = ""
    indent = 4
    dtg = ""

    if queue["key"] and queue["key"] in data and queue["stype"] == "dict":
        k_name = str(data[queue["key"]].split(".")[0])

    if queue["ext"]:
        ext = "." + queue["ext"]

    if queue["flatten"]:
        indent = None

    if queue["dtg"]:
        dtg = datetime.datetime.strftime(datetime.datetime.now(),
                                         "%Y%m%d_%H%M%S")

    elif queue["date"]:
        dtg = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")

    if isinstance(data, dict):
        data = json.dumps(data, indent=indent)

    f_name = queue["prename"] + k_name + queue["postname"] + dtg

    if not f_name:
        f_name = "Default_" + x_name + "_" + r_key

    f_name = os.path.join(queue["directory"], f_name + ext)

    gen_libs.write_file(fname=f_name, mode=queue["mode"], data=data)


def monitor_queue(cfg, log, **kwargs):

    """Function:  monitor_queue

    Description:  Monitor RabbitMQ queue for messages.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.

    """

    def callback(channel, method, properties, body):

        """Function:  callback

        Description:  Process message from RabbitMQ.

        Arguments:
            (input) channel -> Channel properties.
            (input) method -> Delivery properties.
            (input) properties -> Properties of the message.
            (input) body -> Message body.

        """

        log.log_info("callback:  Processing message with Routing Key: %s" %
                     (method.routing_key))
        process_msg(rmq, log, cfg, method, body)
        log.log_info("Deleting message with Routing Key: %s" %
                     (method.routing_key))
        rmq.ack(method.delivery_tag)

    log.log_info("monitor_queue:  Initialize monitoring of queues...")

    for queue in cfg.queue_list:
        rmq = rabbitmq_class.RabbitMQCon(
            cfg.user, cfg.passwd, cfg.host, cfg.port,
            exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
            queue_name=queue["queue"], routing_key=queue["routing_key"],
            x_durable=cfg.x_durable, q_durable=cfg.q_durable,
            auto_delete=cfg.auto_delete)

        log.log_info("Initializing:  Queue: %s, Routing Key: %s" %
                     (queue["queue"], queue["routing_key"]))
        connect_status, err_msg = rmq.create_connection()

        if connect_status and rmq.channel.is_open:
            log.log_info("Initialized RabbitMQ node: %s" % (queue["queue"]))

        else:
            log.log_err("Initialization failed RabbuitMQ: %s -> Msg: %s" %
                        (queue["queue"], err_msg))

        rmq.drop_connection()

    log.log_info("monitor_queue:  Start monitoring queue...")

    # Connect to first queue as only one connection required.
    rmq = rabbitmq_class.RabbitMQCon(
        cfg.user, cfg.passwd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)

    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        log.log_info("Connected to RabbitMQ node")

        # Setup the RabbitMQ Consume callback on multiple queues.
        for queue in cfg.queue_list:
            log.log_info("Monitoring RabbitMQ Queue: %s, Routing Key: %s" %
                         (queue["queue"], queue["routing_key"]))
            rmq.consume(callback, queue=queue["queue"])

        rmq.start_loop()

    else:
        log.log_err("Failed to connnect to RabbuitMQ -> Msg: %s" % (err_msg))


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Set a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dict of function calls and associated options.

    """

    cmdline = gen_libs.get_inst(sys)
    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    cfg, status_flag, err_msg = validate_create_settings(cfg)

    if status_flag:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info("%s:%s Initialized" % (cfg.host, cfg.exchange_name))
        log.log_info("%s" % (str_val))
        log.log_info("Exchange Name:  %s" % (cfg.exchange_name))
        log.log_info("Queue Configuration:")

        for queue in cfg.queue_list:
            log.log_info("\tQueue Name:  %s, Routing Key: %s" %
                         (queue["queue"], queue["routing_key"]))

        log.log_info("To Email:  %s" % (cfg.to_line))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = cfg.exchange_name
            prog_lock = gen_class.ProgramLock(cmdline.argv, flavor_id)

            # Intersect args_array & func_dict to find which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):
                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn("rmq_2_sysmon lock in place for: %s" % (flavor_id))

        log.log_close()

    else:
        print("Error:  Problem in configuration file or directory setup.")
        print(err_msg)


def main(**kwargs):

    """Function:  main

    Description:  Initializes program-wide variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.
        (input) **kwargs:
            argv_list -> List of arguments from another program.

    """

    cmdline = gen_libs.get_inst(sys)
    cmdline.argv = list(kwargs.get("argv_list", cmdline.argv))
    dir_chk_list = ["-d"]
    func_dict = {"-M": monitor_queue}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())

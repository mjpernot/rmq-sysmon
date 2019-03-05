#!/usr/bin/python
# Classification (U)

"""Program:  rmq_2_sysmon.py

    Description:  Process Package Admin emails in RabbitMQ, convert the email
        to a JSON report, and write the JSON report to the sysmon directory.

    Usage:
        rmq_2_sysmon.py -c file -d dir_path [-M] [-v | -h]

    Arguments:
        -M => Monitor and process messages from a RabbitMQ queue.
        -c file => RabbitMQ configuration file.  Required argument.
        -d dir_path => Directory path for option '-c'.  Required argument.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.

    Notes:
        The option to monitor the RabbitMQ is setup to run in an infinite loop
        and can only be killed with a CTRL-C on the command line or shutdown of
        the service.

        RabbitMQ configuration file format (rabbitmq.py).  The configuration
        file format is for the RabbitMQ connection.

            # RabbitMQ Configuration file
            # Classification (U)
            # Unclassified until filled.
            user = "USER"
            passwd = "PASSWORD"
            host = "HOSTNAME"
            # Directory for writing sysmon reports to.
            sysmon_dir = "DIR_PATH"
            # RabbitMQ Exchange name being monitored.
            exchange_name = "EXCHANGE_NAME"
            # RabbitMQ Queue name being monitored.
            queue_name = "QUEUE_NAME"
            # Email address(es) to send non-processed messages to or None.
            # None state no emails are required to be sent.
            to_line = "EMAIL_ADDRESS@DOMAIN_NAME"
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
            message_dir = "message_dir"
            # Directory name for log files.
            log_dir = "logs"
            # File name to program log.
            log_file = "rmq_2_sysmon.log"

    Example:
        rmq_2_sysmon.py -c rabbitmq -d config -M

"""

# Libraries and Global Variables

# Standard
import sys
import os
import socket
import getpass

# Third-party
import json

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

# Version
__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:
        (input) **kwargs:
            None

    """

    print(__doc__)


def validate_create_settings(cfg, **kwargs):

    """Function:  validate_create_settings

    Description:  Validate the configuration settings and creation of certain
        settings.

    Arguments:
        (input) cfg -> Configuration module name.
        (input) **kwargs:
            None
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
        log_name = base_name + "_" + cfg.exchange_name + "_" + cfg.queue_name \
            + ext_name
        cfg.log_file = os.path.join(cfg.log_dir, log_name)

    else:
        err_msg = err_msg + msg
        status_flag = False

    status, msg = gen_libs.chk_crt_dir(cfg.sysmon_dir, write=True, read=True,
                                       no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    return cfg, status_flag, err_msg


def non_proc_msg(rq, log, cfg, data, subj, **kwargs):

    """Function:  non_proc_msg

    Description:  Process non-processed messages.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) data -> Body of message that was not processed.
        (input) **kwargs:
            None

    """

    log.log_info("non_proc_msg:  Processing non-processed message...")
    frm_line = getpass.getuser() + "@" + socket.gethostname()
    f_name = rq.exchange + "_" + rq.queue_name + "_" + gen_libs.get_date() \
        + "_" + gen_libs.get_time() + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    subj = "rmq_2_sysmon: " + subj

    if cfg.to_line:
        log.log_info("Sending email to: %s..." % (cfg.to_line))
        EMAIL = gen_class.Mail(cfg.to_line, subj, frm_line)
        EMAIL.add_2_msg(data)
        EMAIL.send_mail()

    else:
        log.log_warn("No email being sent as TO line is empty.")

    log.log_err("Message was not processed due to: %s" % (subj))
    log.log_info("Saving message to: %s" % (f_path))

    gen_libs.write_file(f_path, data="Exchange: %s, Queue: %s"
                        % (rq.exchange, rq.queue_name))
    gen_libs.write_file(f_path, data=data)


def process_msg(rq, log, cfg, method, body, **kwargs):

    """Function:  process_msg

    Description:  Process message from RabbitMQ queue.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) method -> Delivery properties.
        (input) body -> Message body.
        (input) **kwargs:
            None

    """

    log.log_info("process_msg:  Processing body of message...")

    data = json.loads(body)

    if isinstance(data, dict):

        if "Server" in data:
            f_name = os.path.join(cfg.sysmon_dir,
                                  str(data["Server"].split(".")[0]) +
                                  "_pkgs.json")

            err_flag, err_msg = gen_libs.print_dict(data, json_fmt=True,
                                                    no_std=True, ofile=f_name)

            if err_flag:
                non_proc_msg(rq, log, cfg, data, "Unable to convert to JSON")

        else:
            non_proc_msg(rq, log, cfg, data, "Dictionary does not contain key")

    else:
        non_proc_msg(rq, log, cfg, body, "Non-dictionary format")


def monitor_queue(cfg, log, **kwargs):

    """Function:  monitor_queue

    Description:  Monitor RabbitMQ queue for messages.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (input) **kwargs:
            None

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

        log.log_info("callback:  Processing message...")
        process_msg(rq, log, cfg, method, body)

        log.log_info("Deleting message from RabbitMQ")
        rq.ack(method.delivery_tag)

    log.log_info("monitor_queue:  Start monitoring queue...")

    rq = rabbitmq_class.RabbitMQCon(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    cfg.queue_name, cfg.queue_name,
                                    cfg.x_durable, cfg.q_durable,
                                    cfg.auto_delete)

    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))

    connect_status, err_msg = rq.create_connection()

    if connect_status and rq.channel.is_open:
        log.log_info("Connected to RabbitMQ node")

        # Setup the RabbitMQ Consume callback and start monitoring.
        tag_name = rq.consume(callback)
        rq.start_loop()

    else:
        log.log_err("Failed to connnect to RabbuitMQ -> Msg: %s" % (err_msg))


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Set a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) **kwargs:
            None

    """

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
        log.log_info("Queue Name:  %s" % (cfg.queue_name))
        log.log_info("To Email:  %s" % (cfg.to_line))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = cfg.exchange_name + cfg.queue_name
            prog_lock = gen_class.ProgramLock(sys.argv, flavor_id)

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

    sys.argv = kwargs.get("argv_list", sys.argv)

    dir_chk_list = ["-d"]
    func_dict = {"-M": monitor_queue}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())

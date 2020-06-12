#!/usr/bin/python
# Classification (U)

"""Program:  daemon_rmq_2_sysmon.py

    Description:  Runs the rmq_2_sysmon program as a daemon/service.

    Usage:
        daemon_rmq_2_sysmon.py -a {start|stop|restart} {rmq_2_sysmon_options}

    Arguments:
        -a {start|stop|restart} => start, stop, restart rmq_2_sysmon daemon.
        rmq_2_sysmon_options => See rmq_2_sysmon for all options.
            -c module option from rmq_2_sysmon is required to make the daemon
                pidfile unique for running multiple instances.
            -d full_absolute_directory_path => Directory path for option '-c'.
            -M => Monitor and process messages from a RabbitMQ queue.

        NOTE:  -d option requires the full absolute path the configuration
            directory.  The daemon cannot use a relative path.

    Example:
        daemon_rmq_2_sysmon.py -a start -c rabbitmq -d /full/path/config -M

"""

# Libraries and Global Variables

# Standard
import sys
import time
import os
import psutil

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rmq_2_sysmon
import version

__version__ = version.__version__


class Rmq2SysmonDaemon(gen_class.Daemon):

    """Class:  Rmq2SysmonDaemon

    Description:

    Methods:
        run -> Daemon instance will execute this code when called.

    """

    def run(self):

        """Method:  run

        Description:  Will contain/point to the code to execute when the
            daemon start() or restart() options are executed.

        Variables:
            self.argv_list -> List of command line options and values.

        Arguments:

        """

        while True:
            rmq_2_sysmon.main(argv_list=self.argv_list)
            time.sleep(1)


def is_active(pidfile, proc_name, **kwargs):

    """Function:  is_active

    Description:  Reads a pid from file and determines if the pid is running
        as the process name.

    Arguments:
        (input) pidfile -> Path and file name to a PID file.
        (input) proc_name -> Process name.
        (output) status -> True|False - If process is running.

    """

    status = False

    with open(pidfile, "r") as pfile:
        pid = int(pfile.read().strip())

    if pid:

        for proc in psutil.process_iter():

            if proc.pid == pid and proc.name == proc_name:
                status = True
                break

    return status


def main():

    """Function:  main

    Description:  Initializes program-wide variables, processes command line
        arguments, sets up pidfile, and contols the running of the
        service/daemon.

    Variables:
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    opt_val_list = ["-a", "-c", "-d"]
    opt_req_list = ["-a", "-c", "-d"]
    proc_name = "daemon_rmq_2_sy"

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)
    f_name = "rmq2sysmon_daemon_" + args_array.get("-c", "") + ".pid"
    pid_file = os.path.join(gen_libs.get_base_dir(__file__), "tmp", f_name)
    daemon = Rmq2SysmonDaemon(pid_file, argv_list=cmdline.argv)

    if not arg_parser.arg_require(args_array, opt_req_list):

        if args_array["-a"] == "start":

            if os.path.isfile(pid_file) and is_active(pid_file, proc_name):

                print("Warning:  Pidfile %s exists and process is running."
                      % (pid_file))

            elif os.path.isfile(pid_file):
                os.remove(pid_file)
                daemon.start()

            else:
                daemon.start()

        elif args_array["-a"] == "stop":
            daemon.stop()

        elif args_array["-a"] == "restart":
            daemon.restart()

        else:
            print("Unknown command")
            sys.exit(2)

        sys.exit(0)

    else:
        print("Usage: %s -a start|stop|restart -c module -d directory/config \
{rmq_2_sysmon options}"
              % cmdline.argv[0])
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())

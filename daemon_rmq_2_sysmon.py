#!/usr/bin/python
# Classification (U)

"""Program:  daemon_rmq_2_sysmon.py

    Description:  Run the rmq_2_sysmon program as a daemon.

    Usage:
        daemon_rmq_2_sysmon.py -a {start|stop|restart}
            -c config_file -d dir_path -M

    Arguments:
        -a {start|stop|restart} => start, stop, restart rmq_2_sysmon daemon.
        -c config_file => RabbitMQ configuration file.
        -d dir_path => Directory path for option '-c'.
            NOTE:  This is the absolute path to the directory containing the
                config file.  Relative path will not work.
        -M => Monitor and process messages from a RabbitMQ queue.

    Example:
        daemon_rmq_2_sysmon.py -a start -c rabbitmq -d /path/config -M

"""

# Libraries and Global Variables

# Standard
import sys
import time
import os
import psutil

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from . import rmq_2_sysmon
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import rmq_2_sysmon                                 # pylint:disable=R0402
    import version

__version__ = version.__version__


class Rmq2SysmonDaemon(gen_class.Daemon):

    """Class:  Rmq2SysmonDaemon

    Description:  Class that uses the gen_class.Daemon to run the rmq_2_sysmon
        program as a daemon.

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


def is_active(pidfile, proc_name):

    """Function:  is_active

    Description:  Reads a pid from file and determines if the pid is running
        as the process name.

    Arguments:
        (input) pidfile -> Path and file name to a PID file.
        (input) proc_name -> Process name.
        (output) status -> True|False - If process is running.

    """

    status = False

    with open(pidfile, mode="r", encoding="UTF-8") as pfile:
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
        arguments, sets up pidfile, and contols the running of the daemon.

    Variables:
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.

    """

    opt_val_list = ["-a", "-c", "-d"]
    opt_req_list = ["-a", "-c", "-d"]
    proc_name = "daemon_rmq_2_sy"

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, do_parse=True)
    f_name = "rmq2sysmon_daemon_" + args.get_val("-c", def_val="") + ".pid"
    pid_file = os.path.join(gen_libs.get_base_dir(__file__), "tmp", f_name)
    daemon = Rmq2SysmonDaemon(pid_file, argv_list=sys.argv)

    if args.arg_require(opt_req=opt_req_list):

        if args.get_val("-a") == "start":

            if os.path.isfile(pid_file) and is_active(pid_file, proc_name):

                print(f"Warning:  Pidfile {pid_file} exists and process is"
                      f" possibly running.")

            elif os.path.isfile(pid_file):
                os.remove(pid_file)
                daemon.start()

            else:
                daemon.start()

        elif args.get_val("-a") == "stop":
            daemon.stop()

        elif args.get_val("-a") == "restart":
            daemon.restart()

        else:
            print("Unknown command")
            sys.exit(2)

        sys.exit(0)

    else:
        print(f"Usage: {sys.argv[0]} -a start|stop|restart -c module"
              f" -d directory/config <rmq_2_sysmon_options_here>")
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())

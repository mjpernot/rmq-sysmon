# Python project for processing Package Admin emails in RabbitMQ and send them as JSON reports to the sysmon directory.
# Classification (U)

# Description:
  This program consists of a Python program that processes Package Admin emails in RabbitMQ, converts the emails to a JSON report and write the JSON report to a specified directory.


###  This README file is broken down into the following sections:
 * Features
 * Prerequisites
 * Installation
 * Configuration
 * Running
 * Program Help Function
 * Testing
   - Unit
   - Integration
   - Blackbox


# Features:
 * Process Sysmon reports in RabbitMQ and write JSON reports to sysmon directory.
 * Run the monitor program as a service/daemon.
 * Setup the program up as a service.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - rabbit_lib/rabbitmq_class


# Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-sysmon.git
```

Install/upgrade system modules.

```
cd rmq-sysmon
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create RabbitMQ configuration file.

```
chmod 777 logs message_dir tmp
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.
  * The "user", "passwd", "host", "exchange_name", and "queue_name"  is connection and exchange/queue information to a RabbitMQ node.
  * The "sysmon_dir" is the directory path to where the package admin reports will be written to.
  * The "to_line" is the email address/email alias to the RabbitMQ administrator(s).
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
    - queue_name = "QUEUE_NAME"
    - sysmon_dir = "DIR_PATH"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

(Optional)  Enable program to be ran as a service.  Modify the service script to change the variables to reflect the environment setup.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{USER_ACCT}** with the same name as the user account in rmq_2_sysmon_service.sh script.
  * MOD_LIBRARY is references the configuration file above (e.g. rabbitmq).
  * USER_ACCT is the userid which will execute the daemon and the account must be on the server locally.
  * Change these entries in the rmq_2_sysmon_service.sh file.
    - BASE_PATH="{Python_Project}/rmq-sysmon"
    - USER_ACCOUNT="USER_ACCT"

```
cd ..
cp rmq_2_sysmon_service.sh.TEMPLATE rmq_2_sysmon_service.sh
vim rmq_2_sysmon_service.sh
sudo ln -s {Python_Project}/rmq-sysmon/rmq_2_sysmon_service.sh /etc/init.d/rmq_2_sysmon
sudo chkconfig --add rmq_2_sysmon
sudo chown {USER_ACCT} config/rabbitmq.py
```


# Running
  * Replace **{Python_Project}** with the baseline path of the python program.

### Running as a service.
  * Starting the service.

```
service rmq_2_sysmon start
```

  * Stopping the service.

```
service rmq_2_sysmon stop
```

### Running as a daemon.
  * Starting the daemon.

```
{Python_Project}/rmq-sysmon/daemon_rmq_2_sysmon.py -a start -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
```

  * Stopping the daemon.

```
{Python_Project}/rmq-sysmon/daemon_rmq_2_sysmon.py -a stop -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
```

### Running from the command line.
  * Stating the program.

```
{Python_Project}/rmq-sysmon/rmq_2_sysmon.py -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
```

  * Stopping the program.
```
<Ctrl-C>
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
    `{Python_Project}/rmq-sysmon/rmq_2_sysmon.py -h`
```


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the rmq_2_sysmon.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-sysmon.git
```

Install/upgrade system modules.

```
cd rmq-sysmon
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for rmq_2_sysmon.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rmq-sysmon
```

### Unit:  help_message
```
test/unit/rmq_2_sysmon/help_message.py
```

### Unit:  validate_create_settings
```
test/unit/rmq_2_sysmon/validate_create_settings.py
```

### Unit:  non_proc_msg
```
test/unit/rmq_2_sysmon/non_proc_msg.py
```

### Unit:  process_msg
```
test/unit/rmq_2_sysmon/process_msg.py
```

### Unit:  monitor_queue
```
test/unit/rmq_2_sysmon/monitor_queue.py
```

### Unit:  run_program
```
test/unit/rmq_2_sysmon/run_program.py
```

### Unit:  main
```
test/unit/rmq_2_sysmon/main.py
```

### All unit testing
```
test/unit/rmq_2_sysmon/unit_test_run.sh
```

### Unit test code coverage
```
test/unit/rmq_2_sysmon/code_coverage.sh
```

# Unit test runs for daemon_rmq_2_sysmon.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rmq-sysmon
```

### Unit:  main
```
test/unit/daemon_rmq_2_sysmon/main.py
```

### Unit test code coverage
```
test/unit/daemon_rmq_2_sysmon/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the rmq_2_sysmon.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-sysmon.git
```

Install/upgrade system modules.

```
cd rmq-sysmon
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:
  * Please note that the integration testing will require access to a rabbitmq system to run the tests.

Create RabbitMQ configuration file.

```
chmod 777 tmp
cd test/integration/rmq_2_sysmon
chmod 777 logs message_dir sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.  The "user", "passwd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - sysmon_dir = "DIR_PATH"               -> Change to:  sysmon_dir = "sysmon"
    - exchange_name = "EXCHANGE_NAME"       -> Change to:  exchange_name = "intr-test"
    - queue_name = "QUEUE_NAME"             -> Change to:  queue_name = "intr-test"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME" -> Change to:  to_line = None

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

# Integration test runs for rmq_2_sysmon.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

### Integration tests
```
cd {Python_Project}/rmq-sysmon
test/integration/rmq_2_sysmon/process_msg.py
test/integration/rmq_2_sysmon/validate_create_settings.py
test/integration/rmq_2_sysmon/non_proc_msg.py
test/integration/rmq_2_sysmon/monitor_queue.py
test/integration/rmq_2_sysmon/run_program.py
test/integration/rmq_2_sysmon/main.py
```

### All integration testing
```
test/integration/rmq_2_sysmon/integration_test_run.sh
```

### Integration test code coverage
```
test/integration/daemon_rmq_2_sysmon/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the rmq_2_sysmon.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-sysmon.git
```

Install/upgrade system modules.

```
cd rmq-sysmon
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create RabbitMQ configuration file.

```
chmod 777 tmp
cd test/blackbox/rmq_2_sysmon
chmod 777 logs message_dir sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Change these entries in the rabbitmq.py file.  The "user", "passwd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - sysmon_dir = "DIR_PATH"               -> Change to:  sysmon_dir = "{Python_Project}/test/blackbox/rmq_2_sysmon/sysmon"
    - exchange_name = "EXCHANGE_NAME"       -> Change to:  exchange_name = "blackbox-test"
    - queue_name = "QUEUE_NAME"             -> Change to:  queue_name = "blackbox-test"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME" -> Change to:  to_line = None
    - message_dir = "message_dir"           -> Change to:  message_dir = "test/blackbox/rmq_2_sysmon/message_dir"
    - log_dir = "logs"                      -> Change to:  log_dir = "test/blackbox/rmq_2_sysmon/logs"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

### Blackbox test run for rmq_2_sysmon.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rmq-sysmon
test/blackbox/rmq_2_sysmon/blackbox_test.sh
```


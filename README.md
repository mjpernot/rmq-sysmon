# Python project for processing Admin Monitoring emails in RabbitMQ and save them to a specified directory.
# Classification (U)

# Description:
  Python program that processes administration monitoring emails in RabbitMQ.  The program will process a number of different data types in the report, and will be able to save the report to a specified directory.


###  This README file is broken down into the following sections:
 * Features
 * Prerequisites
 * Installation
 * Configuration
 * System Service
   - systemctl
   - service
 * Running
 * Program Help Function
 * Testing
   - Unit
   - Integration
   - Blackbox


# Features:
 * Process monitoring reports in RabbitMQ and write the reports to a specified directory.
 * Run the monitor program as a service/daemon.
 * Setup the program up as a service.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - Centos 7 (Running Python 2.7):
      -> python-pip
      -> python-devel
    - Redhat 8 (Running Python 3.6):
      -> python3-pip
      -> python3-devel


# Installation:

Install the project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-sysmon.git
cd rmq-sysmon
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create RabbitMQ configuration file.

```
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Make the appropriate changes to connect to a RabbitMQ node/cluster.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - host_list = []
    - exchange_name = "EXCHANGE_NAME"
    - to_line = None
    - message_dir = "DIRECTORY_PATH/message_dir"
    - log_dir = "DIRECTORY_PATH/logs"
    - log_fale = "rmq_2_sysmon.log"

  * Do not change these unless you are familar with RabbitMQ.
    - port = 5672
    - exchange_type = "direct"
    - x_durable = True
    - q_durable = True
    - auto_delete = False
    - heartbeat = 60

  * The next entry is the queue_list, which is the list of queues to monitor.  The queue_list is setup as a list of dictionaries with each dictionary contains an unique combination of queue name and routing key.  Make a copy of the dictionary for each combination and modify it for that queue/routing key setup.
  * Below is a break out of the dictionary.
    - queue:  "QUEUE_NAME" - Name of queue to monitor.
    - routing_key:  "ROUTING_KEY" - Name of the routing key for the queue.
      -> NOTE:  A single queue can have multiple routing keys, but each routing key will have it's own dictionary entry.
    - directory:  "/DIR_PATH" - Directory path to where the report will be written to.
    - prename:  "NAME" - Static pre-file name string.  Default: "", nothing will be added to file name.
    - postname:  "NAME" - Static post-file name string.  Default: "", nothing will be added to file name.
    - key:  "DICT_KEY" - Is the name of a key in a dictionary.  Default: "", nothing will be added to file name.
      -> NOTE:  If the key is present then value will be part of the file name and only applies if message is a dictionary.
    - mode:  "a"|"w" - Write mode to the file: write or append to a file.
    - ext:  "NAME" - Extension name to the file name.  Default: "", nothing will be added to file name.
    - dtg:  True|False - Add a date and time group to the file name.  Format is: YYYYMMDD_YYMMSS.
    - date:  True|False - Add a date to the file name.  Format is: YYYYMMDD.
    - stype:  "any"|"dict"|"list"|"str|file" - Format of the messages that are allowed in the message.
      -> NOTE 1:  Any - Any format is allowed, Dict - Dictionary, List - List, Str - String.
      -> NOTE 2: File - is an attachment and filename inside a dictionary object.
    - flatten:  True|False - Flattens a dictionary format.  Only applicable to dictionary format.
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


```
vim rabbitmq.py
chmod 600 rabbitmq.py
```


# System Service

### Systemctl
(Optional)  Setup and enable program to be ran as a systemctl service.

Modify the systemctl file to change the variables to reflect the environment setup.
  * Change the working directory in rmq-sysmon.service file, if configured differently.
    - WorkingDirectory=/opt/local/rmq-sysmon
  * Change the RabbitMQ configuration file if using a different name.
    - ExecStart=daemon_rmq_2_sysmon.py -a start -c rabbitmq -d ./config -M
    - ExecStop=daemon_rmq_2_sysmon.py -a stop -c rabbitmq -d ./config -M

```
sudo cp {PYTHON_PROJECT}/rmq-sysmon/rmq-sysmon.service /etc/systemd/system
sudo vim /etc/systemd/system/rmq-sysmon.service
sudo enable rmq-sysmon.service
```

### Service
(Optional)  Setup program to be ran as a service.

Modify the service script to change the variables to reflect the environment setup.
  * Change these entries in the rmq_2_sysmon_service.sh file.
    - BASE_PATH="PYTHON_PROJECT/rmq-sysmon"
    - USER_ACCOUNT="USER_NAME"
  * Replace **USER_NAME** with the userid which will execute the daemon and the account must be on the server locally.
  * MOD_LIBRARY is references the configuration file above (e.g. rabbitmq).

```
cp rmq_2_sysmon_service.sh.TEMPLATE rmq_2_sysmon_service.sh
vim rmq_2_sysmon_service.sh
```

Enable program as a service.
```
sudo cp {PYTHON_PROJECT}/rmq-sysmon/rmq_2_sysmon_service.sh /etc/init.d/rmq_2_sysmon
sudo chkconfig --add rmq_2_sysmon
sudo chown USER_NAME config/rabbitmq.py
```


# Running

### Running as a systemctl.

```
systemctl start rmq-sysmon.service
systemctl stop rmq-sysmon.service
```

### Running as a service.

```
service rmq_2_sysmon start
service rmq_2_sysmon stop
```

### Running as a daemon.

```
{Python_Project}/rmq-sysmon/daemon_rmq_2_sysmon.py -a start -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
{Python_Project}/rmq-sysmon/daemon_rmq_2_sysmon.py -a stop -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
```

### Running from the command line.

```
{Python_Project}/rmq-sysmon/rmq_2_sysmon.py -c rabbitmq -d {Python_Project}/rmq-sysmon/config -M
<Ctrl-C>
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
`{Python_Project}/rmq-sysmon/rmq_2_sysmon.py -h`
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/rmq-sysmon
test/unit/rmq_2_sysmon/unit_test_run.sh
test/unit/daemon_rmq_2_sysmon/unit_test_run.sh
```

### Code coverage:
```
cd {Python_Project}/rmq-sysmon
test/unit/rmq_2_sysmon/code_coverage.sh
test/unit/daemon_rmq_2_sysmon/code_coverage.sh
```

# Integration Testing:

### Installation:

Install the project using the procedures in the Installation section.

# Configuration:
  * Please note that the integration testing will require access to a rabbitmq system to run the tests.

Create RabbitMQ configuration file.

```
cd test/integration/rmq_2_sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.  The "user", "passwd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"            -> Change to:  exchange_name = "intr-test"
    - message_dir = "DIRECTORY_PATH/message_dir" -> Change to:  message_dir = "{Python_Project}/rmq-sysmon/test/integration/rmq_2_sysmon/message_dir"
    - log_dir = "DIRECTORY_PATH/logs"            -> Change to:  log_dir = "{Python_Project}/rmq-sysmon/test/integration/rmq_2_sysmon/logs"

  * Have one entry in the queue_list list:
    - "queue_name":                              -> Change value to:  "intr-test"
    - "routing_key":                             -> Change value to:  "intr-test"
    - "directory":                               -> Change value to:  "{Python_Project}/rmq-sysmon/test/integration/rmq_2_sysmon/sysmon"
    - "postname":                                -> Change value to:  "\_pkgs"
    - "key":                                     -> Change value to:  "Server"
    - "ext":                                     -> Change value to:  "json"
    - "stype":                                   -> Change value to:  "dict"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

### Testing:

```
cd {Python_Project}/rmq-sysmon
test/integration/rmq_2_sysmon/integration_test_run.sh
```

### Code coverage:
```
cd {Python_Project}/rmq-sysmon
test/integration/daemon_rmq_2_sysmon/code_coverage.sh
```


# Blackbox Testing:

### Installation:

Install the project using the procedures in the Installation section.

# Configuration:

Create RabbitMQ configuration file.

```
cd test/blackbox/rmq_2_sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.  The "user", "japd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"            -> Change to:  exchange_name = "blackbox-test"
    - to_line = None
    - message_dir = "DIRECTORY_PATH/message_dir" -> Change to:  message_dir = "{PYTHON_PROJECT}/test/blackbox/rmq_2_sysmon/message_dir"
    - log_dir = "DIRECTORY_PATH/logs"            -> Change to:  log_dir = "{PYTHON_PROJECT}/test/blackbox/rmq_2_sysmon/logs"
  * Have one entry in the queue_list list:
    - "queue_name":                              -> Change value to:  "blackbox-test"
    - "routing_key":                             -> Change value to:  "blackbox-test"
    - "directory":                               -> Change value to:  "{PYTHON_PROJECT}/test/blackbox/rmq_2_sysmon/sysmon"
    - "key":                                     -> Change value to:  "Server"
    - "postname":                                -> Change value to:  "\_pkgs"
    - "ext":                                     -> Change value to:  "json"
    - "stype":                                   -> Change value to:  "dict"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

### Testing:

```
cd {Python_Project}/rmq-sysmon
test/blackbox/rmq_2_sysmon/blackbox_test.sh
```


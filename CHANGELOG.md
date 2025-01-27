# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.0.0] - 2025-01-17
Breaking Changes

- Removed Python 2.7 code.
- Removed CentOS service information.
- Updated urllib3==1.26.20
- Added certifi==2024.12.14
- Updated python-lib==4.0.0
- Updated rabbitmq-lib==2.3.0

### Added
- process_queue: Process the message queue.
- convert_data: Convert data from message queue.

### Fixed
- rmq_2_sysmon.process_msg: Converted message body to string as Python 3 returns it as a byte string.

### Changed
- rmq_2_sysmon.process_msg: Changed \_convert_data call to convert_data call.
- rmq_2_sysmon: Converted strings to f-strings.
- daemon_rmq_2_sysmon: Converted strings to f-strings.
- daemon_rmq_2_sysmon: Added "encoding" argument to open() command and set the "mode" to read to open() command.
- Documentation updates.

### Removed
- \_convert_data function.
- \_process_queue function.


## [2.3.4] - 2024-11-19
- Updated python-lib to v3.0.8
- Updated rabbitmq-lib to v2.2.8

### Fixed
- Set chardet==3.0.4 for Python 3.


## [2.3.3] - 2024-11-12
- Updated chardet==4.0.0 for Python 3.
- Added distro==1.9.0 for Python 3.
- Added idna==2.10 for Python 3.
- Updated pika==1.3.1 for Python 3.
- Updated psutil==5.9.4 for Python 3.
- Updated requests==2.25.0 for Python 3.
- Updated urllib3==1.26.19 for Python 3.
- Updated six==1.16.0 for Python 3.
- Updated python-lib to v3.0.7
- Updated rabbitmq-lib to v2.2.7

### Deprecated
- Support for Python 2.7


## [2.3.2] - 2024-09-27
- Updated simplejson==3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated rabbitmq-lib to v2.2.6


## [2.3.1] - 2024-08-15

### Fixed
- \_convert_data:  Base64 decode the data before writing to a file.


## [2.3.0] - 2024-08-01
- Added new stype - file - allows attachment and filename in same message.
- Updated rabbitmq-lib to v2.2.5
- Updated simplejson==3.13.2
- Updated requests==2.25.0
- Added certifi==2019.11.28
- Added idna==2.10
- Added systemctl file for rmq-sysmon daemon.

### Changed
- non_proc_msg: Added Routing Key information to email body.
- run_program: Added date format to the log file name.
- \_convert_data: Added check for stype of file for attachment and associated filename.
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.
- Updates to requirements.txt.
- Documentation updates.


## [2.2.2] - 2024-07-31
- Set urllib3 to 1.26.19 for Python 2 for security reasons.
- Updated rabbitmq-lib to v2.2.4


## [2.2.1] - 2024-03-06
- Updated to work in Red Hat 8
- Updated rabbitmq-lib to v2.2.3
- Updated python-lib to v3.0.3

### Changed
- daemon_rmq_2_sysmon.main: Removed gen_libs.get_inst call and replaced arg_parser with gen_class.ArgParser class.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [2.2.0] - 2023-10-12
- Replaced the arg_parser code with gen_class.ArgParser code.

### Changed
- main, run_program: Replaced the arg_parser code with gen_class.ArgParser code.
- main, run_program: Removed gen_libs.get_inst call.
- Documentation updates.


## [2.1.2] - 2022-12-02
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded rabbitmq-lib to v2.2.1

### Changed
- Converted imports to use Python 2.7 or Python 3.


## [2.1.1] - 2022-06-28
- Upgrade python-lib to v2.9.2

## Fixed
- Upgraded python to v2.8.5 or better to fix daemon error.


## [2.1.0] - 2021-10-04
- Update to work with Pika 1.2.0
- Update to work with RabbitMQ 3.8.2
- Added ability to handle connecting to multiple node cluster

### Fixed
- non_proc_msg:  Increased the granularity of microseconds from 2-digits to 6-digits.
- \_process_queue:  Added microseconds to the datetime group.

### Changed
- monitor_queue:  Replaced rabbitmq_class.RabbitMQCon with rabbitmq_class.create_rmqcon calls.
- non_proc_msg:  Removed extranous characters from the date time group.
- validate_create_settings:  Removed setting message_dir or log_dir to base directory of program directory.
- config/rabbitmq.py.TEMPLATE:  Added heartbeat and host_list entries.
- Removed unnecessary \*\*kwargs in function argument list.
- Documentation updates.


## [2.0.0] - 2020-06-19
- Breaking Change.

- Added ability to monitor multiple RabbitMQ queues with a single run.
- Allow multiple data types within the message body.
- Added multiple routing keys to a single queue for monitoring.

### Added
- \_convert_data:  Private function to convert data.
- \_process_queue:  Private function to process message queue.

### Changed
- process_msg:  Replaced a section of code with call to \_convert_data function.
- \_convert_data:  Replaced a section of code with call to \_process_queue function.
- monitor_queue:  Refactored function to initialize and monitor multiple queues.
- callback:  Added routing key information to log entries.
- process_msg:  Refactored function to handle multiple queues and also multiple data types in the message body.
- non_proc_msg:  Added routing key to parameter list.
- non_proc_msg:  Replaced queue name with routing key to make it unique for message being processed.
- validate_create_settings:  Validate each directory setting for each queue.
- run_program:  Added loop for log information to log all queue name/routing key combinations.
- run_program:  Changed program lock flavor id to the new configuration settings.
- config/rabbitmq.py.TEMPLATE:  Changed format to allow for multiple queues.
- Documentation updates.


## [1.0.1] - 2020-05-29
### Fixed
- main, run_program, daemon_rmq_2_sysmon.main: Fixed handling command line arguments.
- process_msg:  Data to covert can use single or double quotes within the data structure.
- daemon_rmq_2_sysmon.main:  Start up action to check for existing pid file and process.

### Added
- daemon_rmq_2_sysmon.is_active:  Determine if PID is active process on the server.

### Changed
- rmq_2_sysmon_service.sh.TEMPLATE:  Changed format.
- callback, process_msg, non_proc_msg, monitor_queue:  Changed variable name to standard naming convention.
- config/rabbitmq.py.TEMPLATE:  Changed the format for several of the settings.
- monitor_queue:  Changed RabbitMQCon call from positional arguments to keyword arguments.
- process_msg:  Added SyntaxError exception for the data conversion.
- process_msg:  Replaced gen_libs.print_dict with gen_libs.write_file and removed post-if statement.
- Documentation updates.


## [1.0.0] - 2019-11-12
- General Production Release

### Changed
- monitor_queue:  Removed unused variable.

### Fixed
- process_msg:  Convert exception message from a class to a string.

### Changed
- Documentation update.


## [0.3.2] - 2019-09-10
### Fixed
- process_msg:  Capture exception for non-JSON formatted messages.


## [0.3.1] - 2019-06-20
- Allow different JSON report formats to be processed.

### Changed
- process_msg:  Replaced dictionary key with a configuration setting and changed the format of the file name for the JSON report.
- config/rabbitmq.py.TEMPLATE: Added new entries to the rabbitmq configuration template file.


## [0.3.0] - 2019-05-14
- General Field Release

### Fixed
- run_program:  Fixed problem with mutable default arguments issue.


## [0.2.8] - 2019-03-05
### Changed
- main:  Added list() to prevent modifying mutable default argument.
- process_msg, monitor_queue, callback, run_program, main, non_proc_msg:  Refactored code to bring into standard convention.


## [0.2.7] - 2018-11-05
### Changed
- non_proc_msg:  Removed the Email class method create_body as this is incorporated into the class already.
- run_program:  Moved the ProgramLock outside of the function loop so only one lock is created for each run of the program.
- Documentation updates.


## [0.2.6] - 2018-10-05
### Changed
- Documentation updates.


## [0.2.5] - 2018-09-13
### Changed
- Documentation updates.


## [0.2.4] - 2018-09-05
### Changed
- rmq_2_sysmon_service.sh.TEMPLATE:  Added runlevel 2 to default autostart option.


## [0.2.3] - 2018-08-31
### Changed
- process_msg:  Added check to see if "Server" key is in dictionary.


## [0.2.2] - 2018-08-30
### Fixed
- validate_create_settings:  Check for abs path on message_dir and log_dir variables.


## [0.2.1] - 2018-08-30
### Fixed
- process_msg:  Changed dictionary reference to proper key setting.


## [0.2.0] - 2018-08-29
### Changed
- Documentation updates.


## [0.1.1] - 2018-08-28
### Changed
- validate_create_settings:  Pass "no_print" option to gen_libs.chk_crt_dir function calls.

### Removed
- Removed datetime module - not required.


## [0.1.0] - 2018-08-28
### Changed
- Documentation updates.


## [0.0.1] - 2018-08-27
- Initial pre-alpha release.


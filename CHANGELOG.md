# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


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
- daemon_rmq_2_sysmon.main:  Fixed handling command line arguments from SonarQube scan finding.
- run_program: Fixed handling command line arguments from SonarQube scan finding.
- main: Fixed handling command line arguments from SonarQube scan finding.
- process_msg:  Data to covert can use single or double quotes within the data structure.
- daemon_rmq_2_sysmon.main:  Start up action to check for existing pid file and process.

### Added
- daemon_rmq_2_sysmon.is_active:  Determine if PID is active process on the server.

### Changed
- rmq_2_sysmon_service.sh.TEMPLATE:  Changed format.
- monitor_queue:  Changed variable name to standard naming convention.
- callback:  Changed variable name to standard naming convention.
- process_msg:  Changed variable name to standard naming convention.
- non_proc_msg:  Changed variable name to standard naming convention.
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
- main:  Refactored code to bring into standard convention.
- non_proc_msg:  Refactored code to bring into standard convention.
- process_msg:  Refactored code to bring into standard convention.
- monitor_queue:  Refactored code to bring into standard convention.
- callback:  Refactored code to bring into standard convention.
- run_program:  Refactored code to bring into standard convention.


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


# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [1.0.1] - 2020-05-29
### Fixed
- daemon_rmq_2_sysmon.main:  Start up action to check for existing pid file and process.

### Added
- daemon_rmq_2_sysmon.is_active:  Determine if PID is active process on the server.

### Changed
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


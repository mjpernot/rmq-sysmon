# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.2.8] - 2019-03-05
### Changed
- monitor_queue:  Removed unused local variable (tag_name -> _).
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


#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/_convert_data.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/_process_queue.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/help_message.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/process_msg.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/non_proc_msg.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/monitor_queue.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/validate_create_settings.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/run_program.py
coverage run -a --source=rmq_2_sysmon test/unit/rmq_2_sysmon/main.py
coverage run -a --source=daemon_rmq_2_sysmon test/unit/daemon_rmq_2_sysmon/is_active.py
coverage run -a --source=daemon_rmq_2_sysmon test/unit/daemon_rmq_2_sysmon/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i


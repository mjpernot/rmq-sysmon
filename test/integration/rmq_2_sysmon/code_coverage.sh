#!/bin/bash
# Integration test code coverage for rmq_2_sysmon.py module.
# This will run the Python code coverage module against all integration test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/validate_create_settings.py
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/non_proc_msg.py
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/process_msg.py
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/monitor_queue.py
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/run_program.py
coverage run -a --source=rmq_2_sysmon test/integration/rmq_2_sysmon/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m


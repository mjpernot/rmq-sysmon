#!/bin/bash
# Integration testing program for the rmq_2_sysmon.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  rmq_2_sysmon.py"
test/integration/rmq_2_sysmon/process_msg.py
test/integration/rmq_2_sysmon/validate_create_settings.py
test/integration/rmq_2_sysmon/non_proc_msg.py
test/integration/rmq_2_sysmon/monitor_queue.py
test/integration/rmq_2_sysmon/run_program.py
test/integration/rmq_2_sysmon/main.py


#!/bin/bash
# Integration testing program for the rmq_2_sysmon.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  process_msg"
test/integration/rmq_2_sysmon/process_msg.py

echo ""
echo "Integration test:  validate_create_settings"
test/integration/rmq_2_sysmon/validate_create_settings.py

echo ""
echo "Integration test:  non_proc_msg"
test/integration/rmq_2_sysmon/non_proc_msg.py

echo ""
echo "Integration test:  monitor_queue"
test/integration/rmq_2_sysmon/monitor_queue.py

echo ""
echo "Integration test:  run_program"
test/integration/rmq_2_sysmon/run_program.py

echo ""
echo "Integration test:  main"
test/integration/rmq_2_sysmon/main.py


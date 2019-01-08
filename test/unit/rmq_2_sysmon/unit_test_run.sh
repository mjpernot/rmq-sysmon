#!/bin/bash
# Unit testing program for the rmq_2_sysmon.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  help_message"
test/unit/rmq_2_sysmon/help_message.py

echo ""
echo "Unit test:  validate_create_settings"
test/unit/rmq_2_sysmon/validate_create_settings.py

echo ""
echo "Unit test:  non_proc_msg"
test/unit/rmq_2_sysmon/non_proc_msg.py

echo ""
echo "Unit test:  process_msg"
test/unit/rmq_2_sysmon/process_msg.py

echo ""
echo "Unit test:  monitor_queue"
test/unit/rmq_2_sysmon/monitor_queue.py

echo ""
echo "Unit test:  run_program"
test/unit/rmq_2_sysmon/run_program.py

echo ""
echo "Unit test:  main"
test/unit/rmq_2_sysmon/main.py


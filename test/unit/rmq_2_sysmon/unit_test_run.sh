#!/bin/bash
# Unit testing program for the rmq_2_sysmon.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  rmq_2_sysmon.py"
test/unit/rmq_2_sysmon/_convert_data.py
test/unit/rmq_2_sysmon/_process_queue.py
test/unit/rmq_2_sysmon/help_message.py
test/unit/rmq_2_sysmon/validate_create_settings.py
test/unit/rmq_2_sysmon/non_proc_msg.py
test/unit/rmq_2_sysmon/process_msg.py
test/unit/rmq_2_sysmon/monitor_queue.py
test/unit/rmq_2_sysmon/run_program.py
test/unit/rmq_2_sysmon/main.py


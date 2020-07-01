#!/bin/bash
# Blackbox testing program for the rmq_2_sysmon.py program.

BASE_PATH=$PWD

echo "Scenario 1:  rmq_2_sysmon blackbox testing...Startup with no RabbitMQ exchange and empty queue"
test/blackbox/rmq_2_sysmon/rmq_cleanup.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a start
test/blackbox/rmq_2_sysmon/blackbox_test.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a stop
test/blackbox/rmq_2_sysmon/cleanup.py

echo "Scenario 2:  rmq_2_sysmon blackbox testing...Startup with data in RabbitMQ queue"
test/blackbox/rmq_2_sysmon/rmq_cleanup.py
test/blackbox/rmq_2_sysmon/blackbox_publish.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a start
test/blackbox/rmq_2_sysmon/blackbox_test2.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a stop
test/blackbox/rmq_2_sysmon/cleanup.py

echo "Scenario 3:  rmq_2_sysmon blackbox testing...Restart of rmq_2_sysmon service"
test/blackbox/rmq_2_sysmon/rmq_cleanup.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a start
test/blackbox/rmq_2_sysmon/blackbox_test.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a restart
test/blackbox/rmq_2_sysmon/blackbox_test.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a stop
test/blackbox/rmq_2_sysmon/cleanup.py

echo "Scenario 4:  rmq_2_sysmon blackbox testing...Pass non-type report"
test/blackbox/rmq_2_sysmon/rmq_cleanup.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a start
test/blackbox/rmq_2_sysmon/blackbox_test3.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a stop
test/blackbox/rmq_2_sysmon/cleanup.py

echo "Scenario 5:  rmq_2_sysmon blackbox testing...Pass empty report"
test/blackbox/rmq_2_sysmon/rmq_cleanup.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a start
test/blackbox/rmq_2_sysmon/blackbox_test4.py
./daemon_rmq_2_sysmon.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_sysmon/config -M -a stop
test/blackbox/rmq_2_sysmon/cleanup.py


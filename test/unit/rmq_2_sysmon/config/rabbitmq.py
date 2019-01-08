# RabbitMQ Configuration file
# Classification (U)
# Unclassified until filled.
user = "USER"
passwd = "PASSWORD"
host = "HOSTNAME"
# Directory for writing sysmon reports to.
sysmon_dir = "DIR_PATH"
# RabbitMQ Exchange name being monitored.
exchange_name = "EXCHANGE_NAME"
# RabbitMQ Queue name being monitored.
queue_name = "QUEUE_NAME"
# Email address(es) to send non-processed messages to or None.
# None state no emails are required to be sent.
to_line = "EMAIL_ADDRESS"
# RabbitMQ listening port, default is 5672.
port = 5672
# Type of exchange:  direct, topic, fanout, headers
exchange_type = "direct"
# Is exchange durable: True|False
x_durable = True
# Are queues durable: True|False
q_durable = True
# Queues automatically delete message after processing: True|False
auto_delete = False
# Archive directory name for non-processed messages.
message_dir = "message_dir"
# Directory name for log files.
log_dir = "logs"
# File name to program log.
log_file = "rmq_2_sysmon.log"

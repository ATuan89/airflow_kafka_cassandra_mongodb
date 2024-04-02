from kafka import KafkaConsumer
from hdfs import InsecureClient
from hdfs.util import HdfsError

bootstrap_servers = '172.18.0.6:9092,172.18.0.5:9093,172.18.7:9094'  # for local
bootstrap_servers2 = '172.18.0.6:19092,172.18.0.5:19093,172.18.0.7:19094' # for airflow

consumer = KafkaConsumer('log_data',group_id='grp1', bootstrap_servers=bootstrap_servers)
consumer.subscribe(['log_data'])

hdfs_client = InsecureClient('http://172.18.0.1:9870')
hdfs_dir = '/user/kafka-hadoop/'
hdfs_file = hdfs_dir + 'log_data.txt'

# Check if the file exists in HDFS
try:
    hdfs_client.status(hdfs_file)
except HdfsError:
    # If the file doesn't exist, create it
    with hdfs_client.write(hdfs_file, encoding='utf-8') as file:
        print(f'File {hdfs_file} created...')

# Read messages from Kafka topic and insert into HDFS
for message in consumer:
    # Convert message from bytes to string
    log_data = message.value.decode('utf-8')
    print(log_data)

    # Append log data to HDFS file
    print('Starting write to HDFS...')
    with hdfs_client.write(hdfs_file, append=True) as file:
        file.write(log_data + '\n')

# Close consumer
consumer.close()
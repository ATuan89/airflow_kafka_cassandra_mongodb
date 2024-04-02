from kafka import KafkaConsumer
from hdfs import InsecureClient

bootstrap_servers = '172.18.0.6:9092,172.18.0.5:9093,172.18.7:9094'  # for local
bootstrap_servers2 = '172.18.0.6:19092,172.18.0.5:19093,172.18.0.7:19094' # for airflow

consumer = KafkaConsumer('log_data',group_id='grp1', bootstrap_servers=bootstrap_servers)
consumer.subscribe(['log_data'])

hdfs_client = InsecureClient('http://172.18.0.1:9870')
hdfs_dir = '/user/kafka-hadoop/'
hdfs_file = hdfs_dir + 'log_data.txt'

print('Starting consumer...')
for message in consumer:
    # Convert message from bytes to string
    log_data = message.value.decode('utf-8')
    print(log_data)

# Close consumer
consumer.close()
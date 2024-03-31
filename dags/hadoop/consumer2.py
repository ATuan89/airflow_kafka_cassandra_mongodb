from kafka import KafkaConsumer
from hdfs import InsecureClient

bootstrap_servers = '172.18.0.10:9092,172.18.0.8:9093,172.18.0.11:9094'

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

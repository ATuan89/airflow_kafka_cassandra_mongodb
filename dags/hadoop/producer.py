from kafka import KafkaProducer
import time

# Kafka broker address
#bootstrap_servers = '172.18.0.10:19092'
bootstrap_servers = '172.18.0.10:9092,172.18.0.8:9093,172.18.0.11:9094'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Path to the log file
log_file_path = '/opt/airflow/dags/hadoop/log/logch.txt'
log_file_path2 = './log/logch.txt'

# Read log file and send each line as a message to Kafka
with open(log_file_path, 'r') as file:
    for line in file:        
        # Parse each line and create a message
        timestamp, user_id, action, ad_id, campaign_id, platform = line.strip().split(",")
        message = f"{timestamp},{user_id},{action},{ad_id},{campaign_id},{platform}"
	
        producer.send('log_data', message.encode('utf-8'))
        print(f'Message sent to Kafka topic: {message}')

# Close producer
producer.close()
print('All data sent to Kafka topic: log_data')

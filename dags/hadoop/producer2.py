from confluent_kafka import Producer
import ast

# Create a Kafka producer
conf = {'bootstrap.servers': '172.18.0.10:19092,172.18.0.8:19093,172.18.0.11:19094'}
producer = Producer(**conf)

# Topic to send messages to
topic = 'log_data'

# Function to send a message to Kafka
def send_message(producer, msg):
    try:
        producer.produce(topic, msg.encode('utf-8'))
    except Exception as e:
        print(f'Error producing message: {e}')

# Read data from the file
log_file_path = '/opt/airflow/dags/hadoop/log/logch.txt'
log_file_path2 = './log/logch.txt'
with open(log_file_path2, 'r') as file:
    for line in file:
        # Parse the tuple from the line
        try:
            data_tuple = ast.literal_eval(line.strip())
            message = str(data_tuple)
            send_message(producer, message)
            print(f'Sent message: {message}')
        except (ValueError, SyntaxError):
            print(f'Invalid data format: {line.strip()}')

# Flush any remaining messages
producer.flush()
print('All messages sent to Kafka topic: log_data')
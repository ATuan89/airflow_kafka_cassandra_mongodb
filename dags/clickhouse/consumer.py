from confluent_kafka import Consumer, KafkaError
from clickhouse_driver import Client
from datetime import datetime
import logging

print('Consumer started')

# Kafka consumer configuration
KAFKA_BOOTSTRAP_SERVERS = '172.18.0.11:9092,172.18.0.10:9093,172.18.0.9:9094'
KAFKA_BOOTSTRAP_SERVERS_2 = '172.18.0.11:19092,172.18.0.10:19093,172.18.0.9:19094'
KAFKA_GROUP_ID = 'grp1'
KAFKA_TOPIC = 'log_data'

# ClickHouse connection configuration
CLICKHOUSE_HOST = '172.18.0.1'
CLICKHOUSE_PORT = 9000
CLICKHOUSE_USER = 'default'
CLICKHOUSE_PASSWORD = ''
CLICKHOUSE_DATABASE = 'default'

# Create ClickHouse table query
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS logs (
    log_time DateTime,
    user_id UInt32,
    action String,
    ad_id String,
    campaign String,
    source String
) ENGINE = MergeTree()
ORDER BY (log_time);
"""

# ClickHouse insert query
INSERT_QUERY = """
INSERT INTO logs (log_time, user_id, action, ad_id, campaign, source)
VALUES
"""

def main():
    # Initialize ClickHouse client
    clickhouse_client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, user=CLICKHOUSE_USER,
                               password=CLICKHOUSE_PASSWORD, database=CLICKHOUSE_DATABASE)
    
    # Create table if not exists
    clickhouse_client.execute(CREATE_TABLE_QUERY)

    # Kafka consumer configuration
    kafka_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS_2,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    # Create Kafka consumer
    kafka_consumer = Consumer(kafka_config) 

    # Subscribe to Kafka topic
    kafka_consumer.subscribe([KAFKA_TOPIC])
    print(f'Subscribed to Kafka topic: {KAFKA_TOPIC}')
    logging.info(f'Subscribed to Kafka topic: {KAFKA_TOPIC}')

    try:
        print('\ninserting data into ClickHouse...\n')
        while True:
            msg = kafka_consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Parse message
            log_data = eval(msg.value().decode('utf-8'))

            # Format DateTime value
            log_time_formatted = datetime.strptime(log_data[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            insert_query2 = """
                INSERT INTO logs (log_time, user_id, action, ad_id, campaign, source)
                VALUES ('{}', {}, '{}', '{}', '{}', '{}')
                """.format(log_time_formatted, *log_data[1:])
            
            # Execute INSERT query
            clickhouse_client.execute(insert_query2)
            print(f'Inserted data into ClickHouse: {log_data}')
            logging.info(f'Inserted data into ClickHouse: {log_data}')
    except KeyboardInterrupt:
        pass

    finally:
        # Close Kafka consumer
        kafka_consumer.close()
        print('done')
if __name__ == "__main__":
    main()

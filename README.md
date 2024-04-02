# Overview

![image](https://github.com/dogukannulu/airflow_kafka_cassandra_mongodb/assets/91257958/b5ffd185-e046-43cc-ace6-cb7c4069d95f)

# nhớ check inspect network để lấy ip address
# còn port thì lấy từ docker-compose.yml
# 9092, 9093, 9094 là port có thể  chạy local
# 19092, 19093, 19094 là port chạy trên airflow
# consumer, producer hãy chạy test trên local
# consumer2, producer2 hãy chạy test trên airflow

# tạm thời update code cho hadoop, do còn errors
# tạm pending hadoop docker nhưng có vẻ lỗi là chủ sở hữu hadoop không phải root nên nó không chạy, ví dụ : 

#	export HDFS_NAMENODE_USER=blossom
#	export HDFS_DATANODE_USER=blossom
#	export HDFS_SECONDARYNAMENODE_USER=blossom

# 

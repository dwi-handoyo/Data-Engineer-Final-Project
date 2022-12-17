##### KAFKA #####
# Go inside Kafka container instance
docker exec -it kafka-kafka-1 bash

# Go to Kafka bin directory
cd /opt/kafka/bin

# List Topics (check inside /opt/kafka/bin)
kafka-topics.sh --list --bootstrap-server localhost:9092

# Create Topics
kafka-topics.sh --create --topic TopicCurrency --bootstrap-server localhost:9092

# Kafka Consumer CLI
kafka-console-consumer.sh --topic TopicCurrency --from--bootstrap-server localhost:9092

# Open Producer Container
docker exec -it kafka-producer-1 bash

# Open Consumer Container
docker exec -it kafka-consumer-1 bash

# Start Running Producer Instance
docker exec -d 15dea1d93475 bash -c 'python3 main.py --worker 1 --bootstrap-server kafka:9092 --topic TopicCurrency'
python3 main.py --worker 1 --bootstrap-server 192.168.80.2:9092 --topic TopicCurrency
python3 main.py --worker 1 --bootstrap-server kafka:9092 --topic TopicCurrency

# Start Running Consumer Instance
docker exec kafka-consumer-1 bash -c 'python3 main.py --bootstrap-server $KAFKA_HOST --topic $KAFKA_TOPIC --tablename currencies'
python3 main.py --bootstrap-server 192.168.80.2:9092 --topic TopicCurrency --tablename currencies
python3 main.py --bootstrap-server localhost:9092 --topic TopicCurrency --tablename currencies
python3 main.py --bootstrap-servers kafka:9092 --topic TopicCurrency --tablename rate_currency


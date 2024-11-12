from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic
from kafka.errors import KafkaError

KAFKA_BOOTSTRAP: list[str] = ["kafka:9092"]
KAFKA_BROKERS = [
    "kafka-controller-0.kafka-controller-headless.group-01.svc.cluster.local:9092",
    "kafka-controller-1.kafka-controller-headless.group-01.svc.cluster.local:9092",
    "kafka-controller-2.kafka-controller-headless.group-01.svc.cluster.local:9092"
]
DEFAULT_ENCODING = "utf-8"

# Description: Create Kafka topics using the Kafka AdminClient API
def create_topics():
    # Create Kafka topics
    topics = [
        NewTopic(name='test-topic', num_partitions=1, replication_factor=1),
        NewTopic(name='test-topic-2', num_partitions=1, replication_factor=1)
    ]

    # Kafka configuration
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        client_id='test'
    )

    # Create topics
    try:
        admin_client.create_topics(new_topics=topics, validate_only=False)
        print("Topics created successfully")
    except KafkaError as e:
        print(f"Failed to create topics: {e}")

# Description: Produce messages to a Kafka topic
def produce_messages():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        key_serializer=str.encode,
        value_serializer=str.encode
    )

    for i in range(10):
        future = producer.send('test-topic', key=str(i), value=f'message {i}')
        try:
            record_metadata = future.get(timeout=10)
            print(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}]")
        except KafkaError as e:
            print(f"Message delivery failed: {e}")

    producer.flush()

# Description: Consume messages from a Kafka topic
def consume_messages():
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode(DEFAULT_ENCODING)
    )

    try:
        for message in consumer:
            print(f"Received message: {message.value}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    create_topics()
    produce_messages()
    consume_messages()
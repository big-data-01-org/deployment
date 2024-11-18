from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError

KAFKA_BOOTSTRAP = "kafka:9092"
KAFKA_BROKERS = "kafka-controller-0.kafka-controller-headless.group-01.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.group-01.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.group-01.svc.cluster.local:9092"
DEFAULT_ENCODING = "utf-8"

# Description: Create Kafka topics using the Kafka AdminClient API
def create_topics():
    # Create Kafka topics
    topics = [
        'test-topic',
        'test-topic-2'
    ]

    # Kafka configuration
    kafka_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP
    }
    
    admin_client = AdminClient(kafka_config)

    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]

    # Create topics
    fs = admin_client.create_topics(new_topics)

    # Wait for each operation to finish
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")

# Description: Produce messages to a Kafka topic
def produce_messages():
    kafka_config = {
        'bootstrap.servers': KAFKA_BROKERS
    }

    producer = Producer(kafka_config)

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    for i in range(10):
        producer.produce('test-topic', key=str(i), value=f'message {i}', callback=delivery_report)
        producer.poll(0)

    producer.flush()

# Description: Consume messages from a Kafka topic
def consume_messages():
    kafka_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP,
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(kafka_config)
    consumer.subscribe(['test-topic'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.topic()} [{msg.partition()}]")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f"Received message: {msg.value().decode(DEFAULT_ENCODING)}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    create_topics()
    produce_messages()
    consume_messages()
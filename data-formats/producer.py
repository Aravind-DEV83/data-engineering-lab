from confluent_kafka import Producer
import json
import time
import random


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

topic_name = "evolution_topic"

print(f"Started streaming to topic: {topic_name}..")

def publish():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'data-format-producer'
    }
    producer = Producer(config=config)

    try:

        payload = {
            "user_id": random.randint(1000, 9999),
            "action": random.choice(["login", "logout", "purchase", "view_item"]),
            "timestamp": time.time()
        }

        producer.produce(
            topic=topic_name,
            value=json.dumps(payload),
            callback=delivery_report
        )

        producer.poll(0)

        time.sleep(1)
    except KeyboardInterrupt as e:
        print("Streaming stopped by user.")
    finally:
        producer.flush()


if __name__ == "__main__":
    publish()
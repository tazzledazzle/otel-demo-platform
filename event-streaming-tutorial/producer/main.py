#!/usr/bin/env python3
"""Placeholder - will produce synthetic events to Kafka."""
import os
import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "events")
RATE = float(os.environ.get("EVENTS_PER_SEC", "2"))


def main():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            break
        except NoBrokersAvailable:
            print("Waiting for Kafka...")
            time.sleep(2)
    interval = 1.0 / RATE if RATE > 0 else 1.0
    event_types = ["click", "view", "purchase", "signup"]
    n = 0
    print(f"Producing to {TOPIC} at ~{RATE} events/sec")
    while True:
        n += 1
        event = {
            "user_id": f"user_{n % 100}",
            "event_type": event_types[n % len(event_types)],
            "timestamp": time.time(),
            "payload": {"count": n},
        }
        producer.send(TOPIC, value=event)
        if n % 10 == 0:
            producer.flush()
        time.sleep(interval)


if __name__ == "__main__":
    main()

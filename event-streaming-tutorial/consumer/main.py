#!/usr/bin/env python3
"""Placeholder consumer - read from Kafka, call model + decision, log."""
import os
import json
import time
import requests
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "events")
MODEL_URL = os.environ.get("MODEL_SERVICE_URL", "http://localhost:8000")
DECISION_URL = os.environ.get("DECISION_ENGINE_URL", "http://localhost:8001")


def main():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=BOOTSTRAP.split(","),
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
            )
            break
        except NoBrokersAvailable:
            print("Waiting for Kafka...")
            time.sleep(2)
    print("Consumer started")
    for msg in consumer:
        event = msg.value
        try:
            r = requests.post(f"{MODEL_URL}/score", json={"event": event}, timeout=5)
            r.raise_for_status()
            score = r.json().get("score", 0)
        except Exception as e:
            print("Model error:", e)
            score = 0.0
        try:
            r = requests.post(
                f"{DECISION_URL}/decide", json={"event": event, "score": score}, timeout=5
            )
            r.raise_for_status()
            decision = r.json()
        except Exception as e:
            print("Decision error:", e)
            decision = {"action": "error", "reason": str(e)}
        print("event:", event.get("event_type"), "score:", score, "decision:", decision)


if __name__ == "__main__":
    main()

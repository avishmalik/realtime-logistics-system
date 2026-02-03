from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(5):
    event = {
        "order_id": i,
        "status": "PLACED"
    }

    producer.send("orders", event)
    print("Sent:", event)
    time.sleep(1)

producer.flush()

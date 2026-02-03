from kafka import KafkaConsumer, KafkaProducer
import redis
import json
import time

# Kafka Consumer
consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="host.docker.internal:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="order-group"
)
# use bootstrap_servers="kafka:9092" for kafka broker in local

# Kafka Producer (to publish next state)
producer = KafkaProducer(
    bootstrap_servers="host.docker.internal:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
# use bootstrap_servers="kafka:9092" for kafka broker in local

# Redis connection
r = redis.Redis(host="redis", port=6379, decode_responses=True)

STATUS_FLOW = [
    "PLACED",
    "CONFIRMED",
    "PREPARING",
    "OUT_FOR_DELIVERY",
    "DELIVERED"
]

print("Order Processor Running...")

for msg in consumer:
    order = msg.value
    order_id = order["order_id"]
    status = order["status"]

    print(f"Received order {order_id} with status {status}")

    # Save to Redis
    r.set(f"order:{order_id}", status)

    # Move to next status
    if status in STATUS_FLOW:
        idx = STATUS_FLOW.index(status)
        if idx + 1 < len(STATUS_FLOW):
            next_status = STATUS_FLOW[idx + 1]

            time.sleep(2)  # simulate processing

            next_event = {
                "order_id": order_id,
                "status": next_status
            }

            producer.send("orders", next_event)
            producer.flush()

            notification_event = {
                "order_id": order_id,
                "message": f"Order {order_id} is now {next_status}"
            }

            producer.send("order_notifications", notification_event)
            producer.flush()

            print(f"Moved order {order_id} → {next_status}")

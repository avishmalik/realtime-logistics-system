from fastapi import FastAPI
from kafka import KafkaProducer
import redis
import json
import uuid

app = FastAPI()

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="host.docker.internal:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
# use bootstrap_servers="kafka:9092" for kafka broker in local

# Redis
r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.post("/orders")
def create_order():

    order_id = str(uuid.uuid4())[:8]

    event = {
        "order_id": order_id,
        "status": "PLACED"
    }

    producer.send("orders", event)
    producer.flush()

    return {
        "message": "Order created",
        "order_id": order_id
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):

    status = r.get(f"order:{order_id}")

    if not status:
        return {"error": "Order not found"}

    return {
        "order_id": order_id,
        "status": status
    }

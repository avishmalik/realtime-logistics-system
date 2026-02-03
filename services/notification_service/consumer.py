from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "order_notifications",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="notification-group"
)

print("Notification Service Running...")

for msg in consumer:
    notification = msg.value
    
    print("🔔 NOTIFICATION:")
    print(notification["message"])

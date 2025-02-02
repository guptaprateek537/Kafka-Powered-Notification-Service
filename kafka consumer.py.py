from kafka import KafkaConsumer
import json

# Configure Kafka consumer (update bootstrap_servers as needed)
consumer = KafkaConsumer(
    'notification_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='notification_group',
    auto_offset_reset='earliest',  # Start reading at the beginning if no committed offsets
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def process_notification(notification):
    # Replace this print with any processing logic you require.
    print(f"Processing notification: {notification}")

if __name__ == "__main__":
    print("Consumer started. Waiting for messages...")
    for message in consumer:
        process_notification(message.value)

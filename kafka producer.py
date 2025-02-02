from kafka import KafkaProducer
import json
import time

# Configure Kafka producer (update bootstrap_servers as needed)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_notification(notification):
    producer.send('notification_topic', notification)
    producer.flush()  # Make sure the message is delivered immediately
    print(f"Notification sent: {notification}")

if __name__ == "__main__":
    # Simulate continuous notification sending
    while True:
        notification = {
            'user_id': 123,
            'message': 'This is a test notification',
            'timestamp': int(time.time())
        }
        send_notification(notification)
        # For high throughput testing, adjust the sleep duration (e.g., 0.0005 for 2000 events/sec)
        time.sleep(0.001)

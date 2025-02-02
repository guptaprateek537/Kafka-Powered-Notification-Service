from flask import Flask, jsonify, request
import json
import time
from kafka import KafkaProducer

app = Flask(__name__)

# Configure Kafka producer with your broker address (update if necessary)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    # Try to get JSON from the request body; otherwise use a default notification.
    try:
        data = request.get_json(force=True)
    except Exception:
        data = {}
    
    # Use provided data or defaults if not present
    notification = {
        'user_id': data.get('user_id', 1),
        'message': data.get('message', 'Default notification message'),
        'timestamp': int(time.time())
    }
    
    # Send the notification to the Kafka topic "notification_topic"
    producer.send('notification_topic', notification)
    producer.flush()  # Ensure the message is sent immediately
    
    return jsonify({"status": "Notification sent!", "notification": notification}), 200

if __name__ == "__main__":
    # Listen on all network interfaces, port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)

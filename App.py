import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)
load_dotenv()

# Retrieve environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not (TWILIO_ACCOUNT_SID and AUTH_TOKEN and TWILIO_PHONE_NUMBER):
    raise Exception("Please set TWILIO_ACCOUNT_SID, AUTH_TOKEN, and TWILIO_PHONE_NUMBER.")

# Initialize the Twilio client
client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

def send_sms(to_number, message):
    try:
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return sms.sid
    except Exception as e:
        raise Exception(f"Failed to send SMS: {e}")

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided.'}), 400

    message_body = data.get('message')
    if not message_body:
        return jsonify({'error': 'Missing \"message\" parameter.'}), 400

    if message_body.strip().lower() == "hello":
        return jsonify({'message': 'Received hello. No notification triggered.'}), 200
    else:
        to_number = data.get('to')
        if not to_number:
            return jsonify({'error': 'Missing \"to\" parameter for notification.'}), 400

        try:
            sms_message = f"Alert: {message_body}"
            sms_sid = send_sms(to_number, sms_message)
            return jsonify({
                'message': 'Notification triggered. SMS sent successfully.',
                'sid': sms_sid
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

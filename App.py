import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.rest import Client
###load_dotenv()  
app = Flask(__name__)
load_dotenv()
# Hardcoded credentials (for testing only; not recommended for production)
TWILIO_API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
TWILIO_API_KEY_SECRET = os.getenv("TWILIO_API_KEY_SECRET")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not (TWILIO_API_KEY_SID and TWILIO_API_KEY_SECRET and TWILIO_ACCOUNT_SID and TWILIO_PHONE_NUMBER):
    raise Exception("Please set all required Twilio credentials.")

# Initialize the Twilio client using the API Key method.
client = Client(api_key_sid, api_key_secret, account_sid)

def send_sms(to_number, message):
    """
    Send an SMS using Twilio.
    :param to_number: The recipient's phone number in E.164 format (e.g., "+19876543210").
    :param message: The message body to send.
    :return: The SID of the sent SMS.
    """
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
        return jsonify({'error': 'Missing "message" parameter.'}), 400

    if message_body.strip().lower() == "hello":
        return jsonify({'message': 'Received hello. No notification triggered.'}), 200
    else:
        to_number = data.get('to')
        if not to_number:
            return jsonify({'error': 'Missing "to" parameter for notification.'}), 400

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

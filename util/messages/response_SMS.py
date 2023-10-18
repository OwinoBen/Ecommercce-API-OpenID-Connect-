import os
import africastalking
from dotenv import load_dotenv

load_dotenv()


def send_sms_notification(message, phone):
    # Initialize SDK
    username = "Patazoneltd"
    api_key = os.environ.get('AFRICASTALKING_API_KEY')
    # api_key = 'd424f9be92c8dbd0b20d4e8084e37b49d6edf09c44279d8b27f3fc27ad4b1f6b'
    africastalking.initialize(username, api_key)
    # Set your shortCode or senderId
    sender = "patazone"

    mobile = phone[-9:]
    sms = africastalking.SMS
    try:
        response = sms.send(message, ["+254" + mobile], sender)
        print(response)
    except Exception as e:
        print('Encountered an error while sending: %s' % str(e))

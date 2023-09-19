import os
import africastalking
from dotenv import load_dotenv

load_dotenv()


def send_sms_notification(message, phone):
    # Initialize SDK
    username = "Patazone"
    api_key = os.environ.get('AFRICASTALKING_API_KEY')
    africastalking.initialize(username, api_key)

    mobile = phone[-9:]
    sms = africastalking.SMS
    try:
        response = sms.send(message, ["+254" + mobile])
        print(response)
    except Exception as e:
        print('Encountered an error while sending: %s' % str(e))

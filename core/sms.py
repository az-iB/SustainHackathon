from twilio.rest import TwilioRestClient

def sendSMS( message ):
    account = "AC66e097be70f7c18eda6517594fa80cc3"
    token = "ec60fcb4c6ea9084815b9c7925f13b17"
    client = TwilioRestClient(account, token)

    message = client.sms.messages.create(to="+19179713839", from_="+14085602811",
                                         body=message)

sendSMS('Your previous charging spot is occupied right now but we found a new one for you! Address: ')



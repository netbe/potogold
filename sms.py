from twilio.rest import TwilioRestClient

def send_sms(target_number, message):
  account_sid = "AC7e0058368c2e78fde1931b20557cb78c"
  auth_token = "55c4389036bf9067115ce1495f435c22"
  client = TwilioRestClient(account_sid, auth_token)
  #message = client.messages.create(to="004915204062600",from_="+4915735982379",body="test")
  message = client.messages.create(to=target_number,from_="+4915735982379",body=message)

if __name__ == "__main__":
  twil()

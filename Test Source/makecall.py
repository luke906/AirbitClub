# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACe9d8f7def064cdea868bba06b902ee1b"
auth_token = "2088e2d9c761a09e0b00a9fa6d3f0314"
client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+821087821203",
    from_="+82045156136",
    url="http://demo.twilio.com/docs/voice.xml"
)

print(call.sid)
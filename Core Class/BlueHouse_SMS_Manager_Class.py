import base64
import http.client
import json

class SMS_Manager:

    def __init__(self):
        self.appid = 'MTunes_Airbitclub'
        self.apikey = '314ed4d400c411e8b41e0cc47a1fcfae'
        self.address = 'api.bluehouselab.com'
        self.sender = '01087821203'  # FIXME - MUST BE CHANGED AS REAL PHONE NUMBER

        str = self.appid + ':' + self.apikey
        credential = "Basic " + base64.b64encode(str.encode('UTF-8')).decode('ascii').strip()

        self.headers = {
            "Content-type": "application/json;charset=utf-8",
            "Authorization": credential,
        }

    def send_sms(self, str_receiver, str_contents):

        receivers = "['" + str_receiver + "', ]"
        c = http.client.HTTPSConnection(self.address)

        path = "/smscenter/v1.0/sendsms"
        value = {
            'sender': self.sender,
            'receivers': receivers,
            'content': str_contents,
        }
        data = json.dumps(value, ensure_ascii=False).encode('utf-8')

        c.request("POST", path, data, self.headers)
        r = c.getresponse()

        print(r.status, r.reason)
        print(r.read())

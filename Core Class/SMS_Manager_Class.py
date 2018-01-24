import base64
import http.client
import json

appid = 'MTunes_Airbitclub'
apikey = '314ed4d400c411e8b41e0cc47a1fcfae'
address = 'api.bluehouselab.com'

sender = '01087821203'        # FIXME - MUST BE CHANGED AS REAL PHONE NUMBER
receivers = ['01087821203', ] # FIXME - MUST BE CHANGED AS REAL PHONE NUMBERS
content = u'나는 유리를 먹을 수 있어요. 그래도 아프지 않아요'

credential = "Basic "+ base64.encodestring(('%s:%s' % (appid,apikey)).encode()).decode().strip()


headers = {
  "Content-type": "application/json;charset=utf-8",
  "Authorization": credential,
}


c = http.client.HTTPSConnection(address)

path = "/smscenter/v1.0/sendsms"
value = {
    'sender'     : sender,
    'receivers'  : receivers,
    'content'    : content,
}
data = json.dumps(value, ensure_ascii=False).encode('utf-8')

c.request("POST", path, data, headers)
r = c.getresponse()

print(r.status, r.reason)
print(r.read())
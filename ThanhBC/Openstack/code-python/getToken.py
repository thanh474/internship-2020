import requests
import json

payload ={ "auth": {
    "identity": {
        "methods": ["password"],
        "password": {
            "user": {
              "name": "admin",
              "domain": { "name": "Default" },
              "password": "admisn"
            }
          }
        },
        "scope": {
          "project": {
            "name": "admin",
            "domain": { "name": "Default" }
          }
        }
      }
}
# res = requests.post('http://192.168.53.186:5000/v3/auth/tokens',
# 					headers = {'content-type' : 'application/json'},
# 					data= json.dumps(payload))
# print (res.headers)

i = 1
while i < 170000:
  res = requests.post('http://192.168.53.186:5000/v3/auth/tokens',
					headers = {'content-type' : 'application/json'},
					data= json.dumps(payload));
#print (res.headers)
  i += 1
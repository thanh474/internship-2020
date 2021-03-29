import requests
import json

payload ={ "auth": {
    "identity": {
        "methods": ["password"],
        "password": {
            "user": {
              "name": "admin",
              "domain": { "name": "Default" },
              "password": "admin"
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

# res = requests.post('http://192.168.122.3:5000/v3/auth/token',
# 					headers = {'content-type' : 'application/json'},
# 					data= json.dumps(payload))


i = 1
while i < 170000:
  res = requests.post('http://192.168.122.3:5000/v3/auth/token',
					headers = {'content-type' : 'application/json'},
					data= json.dumps(payload));
  i += 1
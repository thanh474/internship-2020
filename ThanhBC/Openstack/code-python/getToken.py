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

res = requests.post('http://10.5.10.134:5000/v3/auth/token',
					headers = {'content-type' : 'application/json'},
					data= json.dumps(payload))

print(res.headers)
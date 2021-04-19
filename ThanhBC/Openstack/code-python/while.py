import requests
import json




def user(num):
      with  open ('user.txt','r') as file:
        for line in file:
              for word in file:
                    print(word.num)

      
payload ={ "auth": {
    "identity": {
        "methods": ["password"],
        "password": {
            "user": {
              "name": "user",
              "domain": { "name": "Default" },
              "password": "admiqn"
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

print (payload['auth'])


print (user())
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
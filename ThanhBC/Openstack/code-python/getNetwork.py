import requests

res= requests.get("http://192.168.53.186:9696/v2.0/networks",
                     headers={'content-type': 'application/json',
                             'X-Auth-Token': 'gAAAAABgeAkG4VcZ3Oi7arhl1Tg9_JLZO2DKENKlmY3f1M_D2YK__RYFrge6VJtCq855eLhw0nP-5Zs9KFzfnASDjLRIqJLHMHrZv8kRz9KLkFvTNWXxN2PvT3j2ry0kVPii8UkXoSVYMF5xNMeI2IPOOXLq9ORJVWNanYYtJTqL_pxfn6pKyZg'
                             },
                  )

print(res.text)
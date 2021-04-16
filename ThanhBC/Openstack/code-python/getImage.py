import requests
import json


# res = requests.get('http://10.5.10.134:9292/v2/images',
#                     headers={'content-type': 'application/json',
#                              'X-Auth-Token': 'gAAAAABgLotmibEps3UKlLRAJQXlSjyweWU3G0eBnjTPagM_8qvri8GpJ58mWqXgoED-Kn-eoPKEHawSRqvyk8RkIaWiAG0bIvCS7wf1FHOfdIdNUF9OydT0xyIuxTq9Z4VGE3Vfa68axQ7JCp9ahzznWap_jItopmg18xVO4coOyRjwvwvggcg'
#                              },
#                    )

# print(res.text)

i = 1
while i < 170000:
    res = requests.get('http://192.168.53.186:9292/v2/images',
                    headers={'content-type': 'application/json',
                             'X-Auth-Token': 'gAAAAABgeAkG4VcZ3Oi7arhl1Tg9_JLZO2DKENKlmY3f1M_D2YK__RYFrge6VJtCq855eLhw0nP-5Zs9KFzfnASDjLRIqJLHMHrZv8kRz9KLkFvTNWXxN2PvT3j2ry0kVPii8UkXoSVYMF5xNMeI2IPOOXLq9ORJVWNanYYtJTqL_pxfn6pKyZg'
                             }
                   );
    i += 1
import requests
import json


res = requests.get('http://10.5.10.134:8774/v2.1/flavors',
                    headers={'content-type': 'application/json',
                             'X-Auth-Token': 'gAAAAABgLotmibEps3UKlLRAJQXlSjyweWU3G0eBnjTPagM_8qvri8GpJ58mWqXgoED-Kn-eoPKEHawSRqvyk8RkIaWiAG0bIvCS7wf1FHOfdIdNUF9OydT0xyIuxTq9Z4VGE3Vfa68axQ7JCp9ahzznWap_jItopmg18xVO4coOyRjwvwvggcg'
                             },
                   );

print(res.text)
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
    res = requests.get('http://192.168.122.3:9292/v2/images',
                    headers={'content-type': 'application/json',
                             'X-Auth-Token': 'gAAAAABgX_Tu-15l02rXUKMS_qHbieObEzJgfB9e-pD37LUQNHMRYq54KeJ1NJQtquy3SJjvFyjHLqfPHctUqZ4NnPP4yE-8TCsOvUE3XUVA0coDdUpM4dhtNDsyCrx1j1HwuNY3e50xOiRuoglbn-UfwKvMvNrN68hl9-lszMHS81jwdZumk5Y'
                             }
                   );
    i += 1
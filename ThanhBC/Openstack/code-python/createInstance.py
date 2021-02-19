import requests
import json

payload= {
    "server": {
        "name": "test2-cirros",
        "imageRef": "7d001a6d-23c8-4344-bd24-86829c138c6f",
        "flavorRef": "3c95aef6-0fba-4d7e-af6f-e3ffde074ea5",
        "networks": [{
            "uuid": "613a8493-f74b-4c80-bde4-39131db6e982"
        }]
    }
}


res = requests.post('http://10.5.10.134:8774/v2.1/servers',
                    headers={'content-type': 'application/json',
                             'X-Auth-Token': 'gAAAAABgLotmibEps3UKlLRAJQXlSjyweWU3G0eBnjTPagM_8qvri8GpJ58mWqXgoED-Kn-eoPKEHawSRqvyk8RkIaWiAG0bIvCS7wf1FHOfdIdNUF9OydT0xyIuxTq9Z4VGE3Vfa68axQ7JCp9ahzznWap_jItopmg18xVO4coOyRjwvwvggcg'
                             },
                    data=json.dumps(payload)
                   )
print(res.text)
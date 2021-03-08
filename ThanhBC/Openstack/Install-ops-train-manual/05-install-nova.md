# Cài đặt nova project 

1. Tạo và phần quyền database cho nova.
```
mysql -u root -p

CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;



GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'thanhbc_nvdb';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' \
  IDENTIFIED BY 'thanhbc_nvdb';

GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'thanhbc_nvdb';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' \
  IDENTIFIED BY 'thanhbc_nvdb';

GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'thanhbc_nvdb';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' \
  IDENTIFIED BY 'thanhbc_nvdb';
```


2. Tạo user nova cho compute service.

```
openstack user create --domain default --password-prompt nova
```


```
openstack role add --project service --user nova admin
```
3. Tạo nova entry
```
openstack service create --name nova \
  --description "OpenStack Compute" compute
```
4. Tạo các endpoint cho nova service.

```
openstack endpoint create --region RegionOne \
  compute public http://controller:8774/v2.1

openstack endpoint create --region RegionOne \
  compute internal http://controller:8774/v2.1

openstack endpoint create --region RegionOne \
  compute admin http://controller:8774/v2.1

```

5. Cài đặt các gói cho nova project.
```
yum install openstack-nova-api openstack-nova-conductor \
  openstack-nova-novncproxy openstack-nova-scheduler
```

6. Cấu hình các thông số trong file cấu hình nova.

```
[DEFAULT]
# ...
enabled_apis = osapi_compute,metadata
transport_url = rabbit://openstack:thanhbc_rabbitmq@controller:5672/
my_ip = 10.5.10.198
use_neutron = true
firewall_driver = nova.virt.firewall.NoopFirewallDriver


[api_database]
# ...
connection = mysql+pymysql://nova:thanhbc_nvdb@controller/nova_api

[database]
# ...
connection = mysql+pymysql://nova:thanhbc_nvdb@controller/nova

[api]
# ...
auth_strategy = keystone

[keystone_authtoken]
# ...
www_authenticate_uri = http://controller:5000/
auth_url = http://controller:5000/
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = thanhbc_nova

[vnc]
enabled = true
# ...
server_listen = $my_ip
server_proxyclient_address = $my_ip


[glance]
# ...
api_servers = http://controller:9292

[oslo_concurrency]
# ...
lock_path = /var/lib/nova/tmp


[placement]
# ...
region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller:5000/v3
username = placement
password = thanhbc_pl
```
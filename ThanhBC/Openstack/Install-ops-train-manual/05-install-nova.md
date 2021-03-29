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


2. Tạo user nova cho compute service với passwork `thanhbc_nv`

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
![](nv-img/nv-endpoint.png)
5. Cài đặt các gói cho nova project.
```
yum install openstack-nova-api openstack-nova-conductor openstack-nova-novncproxy openstack-nova-scheduler openstack-nova-compute -y
```

6. Cấu hình các thông số trong file cấu hình nova.` vim /etc/nova/nova.conf`

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
password = thanhbc_nv

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

[libvirt]
# ...
virt_type = qemu

```

7. Upload dữ liệu từ file cấu hình vào database.


```
su -s /bin/sh -c "nova-manage api_db sync" nova

su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova

su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova

su -s /bin/sh -c "nova-manage db sync" nova
```

Kiểm tra trong database đã lưu các cell chưa.
```
su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova
```

![](nv-img/cell-database.png)

8. Khởi động và bật các service nova chạy cùng hệ thống.

```
systemctl enable \
    openstack-nova-api.service \
    openstack-nova-scheduler.service \
    openstack-nova-conductor.service \
    openstack-nova-novncproxy.service
systemctl restart \
    openstack-nova-api.service \
    openstack-nova-scheduler.service \
    openstack-nova-conductor.service \
    openstack-nova-novncproxy.service \
    libvirtd.service openstack-nova-compute.service

systemctl enable libvirtd.service openstack-nova-compute.service
systemctl start libvirtd.service openstack-nova-compute.service
```

Kiểm tra các service đã hoạt động chưa.
```
systemctl status \
    openstack-nova-api.service \
    openstack-nova-scheduler.service \
    openstack-nova-conductor.service \
    openstack-nova-novncproxy.service
systemctl status libvirtd.service openstack-nova-compute.service
```

![](nv-img/nova-service-1.png)

![](nv-img/nova-service-2.png)


Kiểm tra service trong nova-compute.

![](nv-img/nv-service-compute.png)

Như vậy là ta đã thành công nova project.


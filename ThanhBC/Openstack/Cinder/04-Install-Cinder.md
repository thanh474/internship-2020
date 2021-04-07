# Cài đặt và cấu hình cinder trên 2 node controller và storage.


## Sơ đồ host.
![](cdimg/diagram.png)


## 1. Cấu hình trên controller

### 1.1 Tạo và phân quyền database;

```
mysql -u root -p
```

Tạo database cinder.
```
CREATE DATABASE cinder;

GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'thanhbc_cddb';

GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'thanhbc_cddb';
```
### 1.2 Tạo user và các service.

Tạo user `cinder` với password là `thanhbc_cd`.

```
openstack user create --domain default --password-prompt cinder
```
Add user `cinder` và role `admin`.

```
openstack role add --project service --user cinder admin
```
Tạo service cho `cinderv2` và `cinderv3`.

```
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2

openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3
```

Tạo các Block storage endpoint cho cinderv2 và cinderv3.

```
openstack endpoint create --region RegionOne volumev2 public http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 internal http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 admin http://controller:8776/v2/%\(project_id\)s
```


```
openstack endpoint create --region RegionOne volumev3 public http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 internal http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 admin http://controller:8776/v3/%\(project_id\)s
```
![](cdimg/endpoint.png)


### 1.3 Install và cài đặt cinder.

Tải packages cinder bằng câu lệnh.

```
yum install openstack-cinder -y
```
Chỉnh sửa file cấu hình cinder `/etc/cinder/cinder.conf`

```
[DEFAULT]
# ...
transport_url = rabbit://openstack:thanhbc_rabbitmq@controller
auth_strategy = keystone
my_ip = 10.5.8.239

[database]
# ...
connection = mysql+pymysql://cinder:thanhbc_cddb@controller/cinder


[keystone_authtoken]
# ...
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = thanhbc_cd


[oslo_concurrency]
# ...
lock_path = /var/lib/cinder/tmp
```

Đồng bộ cinder vào databases.
```
su -s /bin/sh -c "cinder-manage db sync" cinder
```
Cài đặt để compute sử dụng block storage. Chỉnh sửa trong file `/etc/nova/nova.conf`

```
[cinder]
os_region_name = RegionOne
```


### 1.4 Khỏi động lại các dịch vụ.


Khởi động lại nova-api
```
systemctl restart openstack-nova-api.service
```

Bật cinder và đặt cinder khởi động cùng hệ thống.

```
systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service
systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
```


## 2. Cài đặt trên storage node

Tải LVM
```
yum install lvm2 device-mapper-persistent-data
```

Bật và khởi động lvm.
```
systemctl enable lvm2-lvmetad.service
systemctl start lvm2-lvmetad.service
```

Tạo 1 physical volume.
```
pvcreate /dev/vdd
```

```
vgcreate cinder-volumes2 /dev/vdd
```
Cấu hình cho LVM sử dụng chính xác volume nào trong file ` /etc/lvm/lvm.conf`

```
devices {
...
filter = [ "a/vdd/", "r/.*/"]
```
Câu lệnh trên cho ta thấy lọc và sử dụng volume vdd còn các volume khác thì loại bỏ.


Tải packages cinder cho storage node.
```
yum install openstack-cinder targetcli python-keystone -y 
```

Cấu hính cinder trong file `/etc/cinder/cinder.conf`.


```
[DEFAULT]
# ...
transport_url = rabbit://openstack:thanhbc_rabbitmq@controller
my_ip = 10.5.9.80
enabled_backends = lvm
glance_api_servers = http://controller:9292
auth_strategy = keystone

[database]
# ...
connection = mysql+pymysql://cinder:thanhbc_cddb@controller/cinder



[keystone_authtoken]
# ...
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = thanhbc_cd

[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes2
target_protocol = iscsi
target_helper = lioadm


[oslo_concurrency]
# ...
lock_path = /var/lib/cinder/tmp
```
Sau khi cấu hình xong lưu lại và khơi động lại cinder-volume.


```
systemctl enable openstack-cinder-volume.service target.service
systemctl start openstack-cinder-volume.service target.service
```

Kiểm tra trên controller node xem đã nhân cinder-volume chưa.

```
openstack volume service list
```
![](cdimg/cd-volume1.png)

## Tạo volume và attach volume vào máy ảo.



# Cài dặt placement-api 

1. Tạo và phân quyền placement database.

```
mysql -u root -p

CREATE DATABASE placement;

GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' \
  IDENTIFIED BY 'thanhbc_pldb';


GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' \
  IDENTIFIED BY 'thanhbc_pldb';

```
2. Tạo user cho service placement với password `thanhbc_pl`.

```
openstack user create --domain default --password-prompt placement
```
Gán role cho placement user.
```
openstack role add --project service --user placement admin
```
3. Tạo các API entry cho placement service.
```
openstack service create --name placement \
  --description "Placement API" placement
```

![](gl-img/api-service.png)

4. Tạo endpoint cho các placement api.
```
openstack endpoint create --region RegionOne \
  placement public http://controller:8778
```

![](gl-img/pl-endpoint-1.png)
```
openstack endpoint create --region RegionOne \
  placement internal http://controller:8778
```

![](gl-img/pl-endpoint-2.png)
```
openstack endpoint create --region RegionOne \
  placement admin http://controller:8778
```

![](gl-img/pl-endpoint-3.png)


5. Cài đặt gói placement api
```
yum install openstack-placement-api -y
```
Chỉnh sửa file cấu hình placement `vim /etc/placement/placement.conf`
```
[placement_database]
# ...
connection = mysql+pymysql://placement:thanhbc_pldb@controller/placement


[api]
# ...
auth_strategy = keystone

[keystone_authtoken]
# ...
auth_url = http://controller:5000/v3
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = placement
password = thanhbc_pl
```

6. Ghi dữ liệu vào database.
```
su -s /bin/sh -c "placement-manage db sync" placement
```

7. Khởi động lại http và kiểm tra kết quả.

```
systemctl restart httpd
```


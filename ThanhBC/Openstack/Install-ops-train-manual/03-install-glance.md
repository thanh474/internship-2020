# Cài đặt glance project.

## Cấu hình database.
```
mysql -u root -p
```
Tạo database và phân quyền cho  glance.
```
CREATE DATABASE glance;

GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
IDENTIFIED BY 'thanhbc_gldb';

```

2. Chạy biến moi trường keystone_admin `vim ~/keystone`
```
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
```

3. Tạo user glance với password là `thanhbc_gl`
```
openstack user create --domain default --password-prompt glance
```
Gán role admin vào user glance và service project.
```
openstack role add --project service --user glance admin
```


Tạo glance service entity
```
openstack service create --name glance \
  --description "OpenStack Image" image
```

4. Tạo image API endpoint.
```
openstack endpoint create --region RegionOne \
  image public http://controller:9292
```

![](gl-img/api-endpoint-1.png)

```
openstack endpoint create --region RegionOne \
  image internal http://controller:9292
```
![](gl-img/api-endpoint-2.png)
```
openstack endpoint create --region RegionOne \
  image internal http://controller:9292
```
![](gl-img/api-endpoint-3.png)

5. Cài đặt cấu hình  openstack-glance.
```
yum install openstack-glance -y
```
Cấu hình file cài đặt glance. `vim /etc/glance/glance-api.conf`

```
[database]
# ...
connection = mysql+pymysql://glance:thanhbc_gldb@controller/glance

[keystone_authtoken]
# ...
www_authenticate_uri  = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = thanhbc_gl

[paste_deploy]
# ...
flavor = keystone


[glance_store]
# ...
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/
```

6. Ghi dữ liệu glacne vào database
```
su -s /bin/sh -c "glance-manage db_sync" glance
```

7. Khỏi động lại service và enable service chạy cùng hệ thống.


```
systemctl enable openstack-glance-api.service
systemctl start openstack-glance-api.service
```
8. Kiểm tra service glance
```
systemctl status openstack-glance-api.service
```

![](gl-img/status-glance.png)


Như vậy là ta đã cấu hình thành công glance project.

9. Kiểm tra bằng cách tạo một image.

Tải file source image cirros.
```
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
```
Upload images lên glance service.
```
glance image-create --name "cirros" \
  --file cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --visibility public
```
![](gl-img/gl-image.png)


Kiểm tra image tron glance service.
```
glance image-list
```

![](gl-img/gl-list.png)

Như vậy là ta đã cấu hình xong glance project.

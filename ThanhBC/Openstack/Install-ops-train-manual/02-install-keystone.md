# Cài đặt keystone project.

## 1 Tạo database cho Keystone.

Truy cập vào database với user root.

```
mysql -u root -p
``` 
Password được cài đặt từ ban đâu ở đây là `admin`

Tạo database `keystone`
```
MariaDB [(none)]> CREATE DATABASE keystone;
```
Gán quyền truy cập vào `keystone`.
```
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
IDENTIFIED BY 'thanhbc_ksdb';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
IDENTIFIED BY 'thanhbc_ksdb';
```

Thoát database và cài đặt gói openstack-keystone.

Cài đặt repo của openstack train version
```
yum install centos-release-openstack-train -y
yum install openstack-keystone httpd mod_wsgi -y 
```
Keystone dc viết bằng python nên ta cài đặt python và openstack-client.
```
yum install gcc python python-devel python2-pip -y
pip install python-openstackclient
pip install --ignore-installed PyYAML
pip install --upgrade "pip < 21.0"
curl https://bootstrap.pypa.io/2.7/get-pip.py --output get-pip.py | 
```

sử dung `vim` để mở file`/etc/keystone/keystone.conf` và sửa  theo các dòng như sau.
```
[database]
# ...
connection = mysql+pymysql://keystone:thanhbc_ksdb@controller/keystone

[token]
# ...
provider = fernet
```
Điền vào sơ sở dữ liệu database keystone.
```
su -s /bin/sh -c "keystone-manage db_sync" keystone
```

Tiếp theo ta  khởi tạo khóa Fernet.
```
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```


Bootstrap dịch vụ identity bằng lệnh.
```
keystone-manage bootstrap --bootstrap-password admin \
  --bootstrap-admin-url http://controller:5000/v3/ \
  --bootstrap-internal-url http://controller:5000/v3/ \
  --bootstrap-public-url http://controller:5000/v3/ \
  --bootstrap-region-id RegionOne
```

## 2.Cấu hình http server.

Cấu hình file `/etc/httpd/conf/httpd.conf` và sửa các thông số sau.
```
ServerName controller
```
Tạo link thư mục `/usr/share/keystone/wsgi-keystone.conf`

```
ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/
```

### 3 Kiểm tra cài đặt.

Tiến hành khởi động và enable httpd 
```
systemctl enable httpd.service
systemctl start httpd.service
```

Kiểm tra xem keystone đã hoạt động hay chưa.



Ta thêm các biến môi trường như sau:
```
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
```

Sau đó sử dụng lệnh `openstack token issue`. 

Nếu trả về kết qủa như sau thì đã thành công.
![](ks-img/token-issue.png).

Nếu kết quả trả về là đoạn code.
```
Internal Server Edbrror (HTTP 500)
```

Thì ta cần phân quyền cho keystone bằng lệnh.
```
chown -R keystone:keystone /etc/keystone/
```

Khởi động lại http và kiểm tra lại kết quả.



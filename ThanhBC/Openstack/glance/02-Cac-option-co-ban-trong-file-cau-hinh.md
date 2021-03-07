# Tìm hiểu file cấu hình của glance

## Mục lục

[1. File glance-api.conf](#api)

[2. File glance-registry.conf](#registry)

[3. File log của glance](#log)

--------

Glance có 2 daemon chạy ẩn đó là glance-api và glance-registry.

<a name="api"></a>
### 1. File glance-api.conf

- Nằm tại thư mục `/etc/glance/glance-api.conf`
![](glimg/glance-file-config.png)

- Tại section [database], cấu hình để kết nối tới database:

``` sh
[database]
# ...
connection = mysql+pymysql://glance:5e9e6b9bc82f4986@192.168.122.73/glance
```
Trong đó :
- `mysql+pymysql`: backend được sử dụng
- `glance` : user sử dụng két nối.
- `5e9e6b9bc82f4986`: password của user glance sử dụng để đăng nhập database.
- `192.168.122.73`: ip host hoặc có thể để tên host.


- Section [keystone_authtoken] và [paste_deploy] chứa các cấu hình để kết nối tới identity service:

``` sh
[keystone_authtoken]
# ...
auth_uri = http://192.168.122.73:5000
auth_url = http://192.168.122.73:35357
memcached_servers = 192.168.122.73:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = GLANCE_PASS

[paste_deploy]
# ...
flavor = keystone
```

- Section [glance_store] chứa cấu hình về kiểu lưu trữ image cũng như nơi chứa image file.

``` sh
[glance_store]
# ...
stores = file,http,swift
default_store = file
filesystem_store_datadir = /var/lib/glance/images/
```

- Ở đây có 2 loại stores được sử dụng và mặc định sẽ sử dụng file system. Bạn có thể cấu hình để lưu trữ trên nhiều nơi khác nhau theo cấu trúc:

`filesystem_store_datadirs=PATH:PRIORITY`

Trong đó:

PATH là đường dẫn tới thư mục chứa image và PRIORITY là mức độ ưu tiên.

Ví dụ:

``` sh
filesystem_store_datadirs = /var/glance/store
filesystem_store_datadirs = /var/glance/store1:100
```

<a name="registry"></a>
### 2. File glance-registry.conf

- Tương tự như file `glance-api.conf`, file `glance-registry.conf` cũng được lưu tại thư mục `/etc/glance`. 

![](glimg/glance-file-registry.png)

Đồng thời nó cũng chứa cấu hình để access database cũng như identity service:

``` sh
[database]
# ...
connection = mysql+pymysql://glance:GLANCE_DBPASS@192.168.122.73/glance

[keystone_authtoken]
# ...
auth_uri = http://192.168.122.73:5000
auth_url = http://192.168.122.73:35357
memcached_servers = 192.168.122.73:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = 804ddb0da4ab4667

[paste_deploy]
# ...
flavor = keystone
```

**Lưu ý:** Trên đây chỉ là những cấu hình cơ bản tối thiểu mà người dùng cần thực hiện trong quá trình cài đặt glance, xem thêm về các tùy chọn cấu hình có thể thực hiện [tại đây](https://docs.openstack.org/developer/glance/configuring.html).

<a name="log"></a>
### 3. File log của glance

- Section [DEFAULT] chứa đường dẫn tới file và thư mục log của glance:

``` sh
[DEFAULT]
log_file = /var/log/glance/api.log
log_dir = /var/log/glance
```

- File `glance-api.log` ghi lại lịch sử truy cập api server


![](glimg/glance-log.png)

Đây là log khởi tạo một images trong glance.


- File `glance-registry.log` ghi lại lịch sử liên quan tới registry server.

- Bạn có thể thay đổi file lưu lại log bằng cách chỉnh sửa file cấu hình, sau đó khởi động lại glance-api server bằng câu lệnh:

`glance-control api start glance-api.conf`
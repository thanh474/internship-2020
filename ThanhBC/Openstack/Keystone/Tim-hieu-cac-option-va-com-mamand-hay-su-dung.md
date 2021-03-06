# Tìm hiểu các option cơ bản của keystone và các command hay sử dụng.


## 1. Các option cơ bản trong file cấu hình keystone.

Các file quan trọng trong keystone project.
- `/etc/keystone/keystone.conf`: file cấu hình của keystone.
- `/var/log/keystone/keystone.log`: file log của keystone.

## 2. Cấu trúc file config keystone

- OpenStack sử dụng INI file format cho file config. INI file là một file text đơn giản thể hiện các options theo các cặp giá trị key = value, chúng được nhóm lại thành các section.

- Các tùy chọn cài đặt được nhóm lại thành các section. Thông thường hầu hết các file config của OpenStack đều có 2 section [DEFAULT] và [database]

- Section DEFAULT chứa hầu hết các tùy chọn cấu hình. Các dòng bắt đầu với kí tự # là các comments.
## 3. Các option cơ bản được sử dụng khi cấu hình cài đặt keystone.

### 3.1 session DEFAULT.
```
public_endpoint=http://127.0.0.1:5000
```
Địa chỉ để các user trong keystone có khả năng truy cập keystone.
```
log_dir=/var/log/keystone
```
Nơi lưu trữ log của keystone.


### 3.2 session database.

```
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@192.168.122.73/keystone
```
Cấu hình truy cập database cho keystone.

Giải thích:

- `mysql+pymysql`: backend được sử dụng
- `keystone`: user sử dụng két nối.
- `KEYSTONE_DBPASS`: password của user keystone sử dụng để đăng nhập db..
- `192.168.122.73`: ip host hoặc có thể để tên host.


### 3.3 session token.

```
provider=fernet
```
Keystone sử dụng token loại fernet để cung cấp token cho các user và project khác sử dụng.
```
expiration=3600
```
Thời gian hết hạn của 1 token fernet.
```
revoke_by_id=True
```
Sử dụng cho qua trình rotate và cấp phát lại token.

### 3.4 Các option nâng cao.


## 4. Các command hay sử dụng trong keystone.
Để làm việc với keystone hay bất cứ một service nào khác thì bạn cần phải khai báo thông tin credential.

Ta có thể lưu các thông tin này thành 1 file source để lần sau gọi sử dụng 1 cách dễ dàng.
`vim /root/keystone_admin`
```
unset OS_SERVICE_TOKEN
    export OS_USERNAME=admin
    export OS_PASSWORD='admin'
    export OS_REGION_NAME=RegionOne
    export OS_AUTH_URL=http://192.168.122.73:5000/v3
    export PS1='[\u@\h \W(keystone_admin)]\$ '

export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3
```

Sau khi khai báo các biến môi trường ta có thể lấy token bằng câu lệnh sau.
```
openstack token issue
```
![](ksimg/token-issue2.png)

Ta có thể thấy token trong hàng `id`.

## 4.2 Các lênh làm việc với user, group, project, role, domain.

### 4.2.1 Các thao tác với domain 
Tao mới, xóa , show domain.
```
openstack domain create <tên domain>
openstack domain delete <tên domain>
openstack domain list
```
![](ksimg/domain-cmd.png)

Xem thêm về các câu lệnh [tại đây](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html)

### 4.2.2. Các thao tác với user.
Tạo mới, xóa, show list user.
```
openstack user create <Ten_user> --domain <Ten_domain>  --description "<Mieu_ta_user>"

openstack user delete --domain <Ten_domain> <Ten_user>

openstack user list
```
![](ksimg/user-cmd.png)

Xem thêm về các câu lệnh [tại đây](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html)


### 4.2.3. Các thao tác với Project
Tạo mới, xóa, show list project.
```
openstack project create <Ten_project> --domain <Ten_domain>  --description "<Mieu_ta_projec>"

openstack project delete --domain <Ten_domain> <Ten_project>

openstack project list

```
![](ksimg/project-cmd.png)

### 4.2.4 Các thao tác với role 
Tạo mới, gán , xóa, show list role.
```
openstack role create --domain <Ten_domain> <Ten_role>

openstack role add --domain <Ten_domain> --project <Ten_project> --user <Ten_user>

openstack role delete --domain <Ten_domain> <role>

openstack role list

```

Xem thêm về các câu lệnh [tại đây](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html)
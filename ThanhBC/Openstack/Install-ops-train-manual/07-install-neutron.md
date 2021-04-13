# Cấu hình network trong openstack với neutron project.
## 1. Tạo và cấu hình databases.

Tạo databases cho neutron.
```
mysql -u root -p

CREATE DATABASE neutron;

GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'thanhbc_ntdb';

GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'thanhbc_ntdb';
```
## 2. Tạo user và endpoint cho neutron.
Tạo user neutron với password `thanhbc_nt`
```
openstack user create --domain default --password-prompt neutron
```
Add role  admin vào neutron user.
```
openstack role add --project service --user neutron admin
```
Tạo service cho neutron.
```
openstack service create --name neutron \
  --description "OpenStack Networking" network
```

Tạo các endpoint.
```
openstack endpoint create --region RegionOne \
  network public http://controller:9696

openstack endpoint create --region RegionOne \
  network internal http://controller:9696

openstack endpoint create --region RegionOne \
  network admin http://controller:9696
```
![](nt-img/nt-endpoint.png)

## 3. Cấu hình network.

Cài đặt các thành phần trong network.
```
yum install openstack-neutron openstack-neutron-ml2 \
  openstack-neutron-linuxbridge ebtables -y
```

Cấu hình file `/etc/neutron/neutron.conf`.


```
[DEFAULT]
# ...
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:thanhbc_rabbitmq@controller
auth_strategy = keystone
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true


[database]
# ...
connection = mysql+pymysql://neutron:thanhbc_ntdb@controller/neutron


[keystone_authtoken]
# ...
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = thanhbc_nt

[nova]
# ...
auth_url = http://controller:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = nova
password = thanhbc_nv

[oslo_concurrency]
# ...
lock_path = /var/lib/neutron/tmp
```

Cấu hình Modular Layer 2 Plug-in `/etc/neutron/plugins/ml2/ml2_conf.ini`

```
[ml2]
# ...
type_drivers = flat,vlan,vxlan

tenant_network_types = vxlan

mechanism_drivers = linuxbridge,l2population

extension_drivers = port_security

[ml2_type_flat]
# ...
flat_networks = provider

[ml2_type_vxlan]
# ...
vni_ranges = 1:1000

[securitygroup]
# ...
enable_ipset = true
```
Cấu hình Linux bridge agent `/etc/neutron/plugins/ml2/linuxbridge_agent.ini`
```
[linux_bridge]
physical_interface_mappings = provider:eth0

[vxlan]
enable_vxlan = true
local_ip = 10.5.10.198
l2_population = true

[securitygroup]
# ...
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

Cấu hình Layer-3 agent `/etc/neutron/l3_agent.ini`
```
[DEFAULT]
# ...
interface_driver = linuxbridge
```

Cấu hình DHCP agent `/etc/neutron/dhcp_agent.ini`

```
[DEFAULT]
# ...
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
```
## 4. Cấu hình metadata agent.
Cấu  hình thêm vào file `/etc/neutron/metadata_agent.ini`
```
[DEFAULT]
# ...
nova_metadata_host = controller
metadata_proxy_shared_secret = METADATA_SECRET
```

## 5. Cấu hình Compute service sử dụng Networking service.

Cấu hình thêm các dòng sau vào file `/etc/nova/nova.conf`
```
[neutron]
auth_url = http://controller:5000
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = neutron
password = thanhbc_nt
service_metadata_proxy = true
metadata_proxy_shared_secret = METADATA_SECRET
```

## 6. Cài đặt symbol link và đồng bộ data conf vào database.

Tạo symbol link cho ML2 Plug-in.
```
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
```
Đồng bộ dữ liệu vào database.
```
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```

Khởi động lại nova api service.
```
systemctl restart openstack-nova-api.service
```

Enable và khởi động các service trong neutron.
```
systemctl enable neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service neutron-l3-agent.service

systemctl restart neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service neutron-l3-agent.service
```

Kiểm tra lại trạng thái hoạt động các service 
```
systemctl status neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service neutron-l3-agent.service
```
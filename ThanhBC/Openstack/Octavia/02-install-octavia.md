# Các bước cài đặt octavia trên train 


## 1. tạo database cho octavia
```
CREATE DATABASE octavia;
GRANT ALL PRIVILEGES ON octavia.* TO 'octavia'@'localhost'  IDENTIFIED BY 'thanhbc_otdb';
GRANT ALL PRIVILEGES ON octavia.* TO 'octavia'@'%' IDENTIFIED BY 'thanhbc_otdb';
```

## 2. Tạo user, role và service cho octavia

Tạo user octavia với password là `thanhbc_otdb`
```
openstack user create --domain default --password-prompt octavia 
```

Gán role và tạo service octavia
```
openstack role add --project admin --user octavia admin
openstack service create --name octavia --description "OpenStack Octavia" load-balancer
```
## 3. Tạo endpoint 
```
openstack endpoint create --region RegionOne load-balancer public http://controller:9876
openstack endpoint create --region RegionOne load-balancer internal http://controller:9876
openstack endpoint create --region RegionOne load-balancer admin http://controller:9876
```
## 4. Taoj image amphora từ resource, upload image amphora và tạo flavor.



## 5. Cài các gói octavia components.


## 6. Tạo các chứng chỉ.

### 6.1 tạo thư mục certs
```
cd
mkdir certs
chmod 700 certs
cd certs
```
### 6.2 tạo file root CA

`vim openssl.conf`

```
# OpenSSL root CA configuration file.

[ ca ]
# `man ca`
default_ca = CA_default

[ CA_default ]
# Directory and file locations.
dir               = ./
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

# The root key and root certificate.
private_key       = $dir/private/ca.key.pem
certificate       = $dir/certs/ca.cert.pem

# For certificate revocation lists.
crlnumber         = $dir/crlnumber
crl               = $dir/crl/ca.crl.pem
crl_extensions    = crl_ext
default_crl_days  = 30

# SHA-1 is deprecated, so use SHA-2 instead.
default_md        = sha256

name_opt          = ca_default
cert_opt          = ca_default
default_days      = 3650
preserve          = no
policy            = policy_strict

[ policy_strict ]
# The root CA should only sign intermediate certificates that match.
# See the POLICY FORMAT section of `man ca`.
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
# Options for the `req` tool (`man req`).
default_bits        = 2048
distinguished_name  = req_distinguished_name
string_mask         = utf8only

# SHA-1 is deprecated, so use SHA-2 instead.
default_md          = sha256

# Extension to add when the -x509 option is used.
x509_extensions     = v3_ca

[ req_distinguished_name ]
# See <https://en.wikipedia.org/wiki/Certificate_signing_request>.

# Optionally, specify some defaults.
countryName_default             = US
stateOrProvinceName_default     = Oregon
localityName_default            =
0.organizationName_default      = OpenStack
organizationalUnitName_default  = Octavia
emailAddress_default            =
commonName_default              = example.org

[ v3_ca ]
# Extensions for a typical CA (`man x509v3_config`).
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ usr_cert ]
# Extensions for client certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = client, email
nsComment = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection

[ server_cert ]
# Extensions for server certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[ crl_ext ]
# Extension for CRLs (`man x509v3_config`).
authorityKeyIdentifier=keyid:always
```

### 6.3 Tạo thư mục CA cho client và server.

```
mkdir client_ca
mkdir server_ca
```

### 6.4 Tạo server certs

```
cd server_ca
mkdir certs crl newcerts private
chmod 700 private
touch index.txt
echo 1000 > serial
```


Tạo CA key với password là `admin`
```
openssl genrsa -aes256 -out private/ca.key.pem 4096
chmod 400 private/ca.key.pem

openssl req -config ../openssl.cnf -key private/ca.key.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem
```
### 6.5 Tạo client certs

```
cd ../client_ca
mkdir certs crl csr newcerts private
chmod 700 private
touch index.txt
echo 1000 > serial
```

Tạo CA với password là `admin`
```
openssl genrsa -aes256 -out private/ca.key.pem 4096
chmod 400 private/ca.key.pem
openssl req -config ../openssl.cnf -key private/ca.key.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem
openssl genrsa -aes256 -out private/client.key.pem 2048
openssl req -config ../openssl.cnf -new -sha256 -key private/client.key.pem -out csr/client.csr.pem
openssl ca -config ../openssl.cnf -extensions usr_cert -days 7300 -notext -md sha256 -in csr/client.csr.pem -out certs/client.cert.pem

openssl rsa -in private/client.key.pem -out private/client.cert-and-key.pem

cat certs/client.cert.pem >> private/client.cert-and-key.pem
```

### 6.6 Tạo file cert cho octavia
```
cd /root/certs
mkdir /etc/octavia/certs
chmod 700 /etc/octavia/certs
cp server_ca/private/ca.key.pem /etc/octavia/certs/server_ca.key.pem
chmod 700 /etc/octavia/certs/server_ca.key.pem
cp server_ca/certs/ca.cert.pem /etc/octavia/certs/server_ca.cert.pem
cp client_ca/certs/ca.cert.pem /etc/octavia/certs/client_ca.cert.pem
cp client_ca/private/client.cert-and-key.pem /etc/octavia/certs/client.cert-and-key.pem
chmod 700 /etc/octavia/certs/client.cert-and-key.pem
chown -R octavia.octavia /etc/octavia/certs
```

## 6.7 Tạo security group và rule
```
. $HOME/octavia-openrc
openstack security group create lb-mgmt-sec-grp
openstack security group rule create --protocol icmp lb-mgmt-sec-grp
openstack security group rule create --protocol tcp --dst-port 22 lb-mgmt-sec-grp
openstack security group rule create --protocol tcp --dst-port 9443 lb-mgmt-sec-grp
openstack security group create lb-health-mgr-sec-grp
openstack security group rule create --protocol udp --dst-port 5555 lb-health-mgr-sec-grp
```
### 6.8 Tạo ssh key
/root/.ssh/octavia_ssh_key

```
ssh-keygen 
openstack keypair create --public-key ~/.ssh/octavia_ssh_key mykey

```

### 6.9 Tạo file dhcp.
```

cd $HOME
sudo mkdir -m755 -p /etc/dhcp/octavia
sudo cp octavia/etc/dhcp/dhclient.conf /etc/dhcp/octavia
```

### 6.10 Tạo network lb-mgmt
```
OCTAVIA_MGMT_SUBNET=172.16.0.0/12
OCTAVIA_MGMT_SUBNET_START=172.16.0.100
OCTAVIA_MGMT_SUBNET_END=172.16.31.254

OCTAVIA_AMP_NETWORK_ID=$(neutron net-create lb-mgmt-net | awk '/ id / {print $4}')

neutron subnet-create --name lb-mgmt-subnet --allocation-pool start=$OCTAVIA_MGMT_SUBNET_START,end=$OCTAVIA_MGMT_SUBNET_END lb-mgmt-net $OCTAVIA_MGMT_SUBNET

id_and_mac=$(neutron port-create --name octavia-health-manager-listen-port --binding:host_id=<network_node_host_name> lb-mgmt-net | awk '/ id | 
mac_address / {print $4}')

MGMT_PORT_ID=${id_and_mac[0]}

MGMT_PORT_MAC=${id_and_mac[1]}

MGMT_PORT_IP=$(neutron port-show $MGMT_PORT_ID | awk '/ "ip_address": / {print $7; exit}' | sed -e 's/"//g' -e 's/,//g' -e 's/}//g')

(On network node):

sudo ovs-vsctl -- --may-exist add-port br-int o-hm0 -- set Interface o-hm0 type=internal -- set Interface o-hm0 external-ids:iface-status=active -- set Interface o-hm0 external-ids:attached-mac=$MGMT_PORT_MAC -- set Interface o-hm0 external-ids:iface-id=$MGMT_PORT_ID

sudo ip link set dev o-hm0 address $MGMT_PORT_MAC

sudo dhclient -v o-hm0
```

### 6.11 Cấu hình file `/etc/octavia/octavia.conf`

`vim /etc/octavia/octavia.conf`
```


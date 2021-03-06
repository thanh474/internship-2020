mysql -u root -p



CREATE DATABASE glance;


GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
  IDENTIFIED BY 'thanhbc_gldb';


openstack user create --domain default --password-prompt glance
#!/bin/bash -xe

# version: 14Apr2020

#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php mysql
sudo chkconfig httpd on
sudo service httpd start
sudo yum install -y mysql57 curl

# Ping github
curl "https://github.com/miztiik"

# To Connect to DB
# mysql -u {User_name} -p -h {RDS_End_Point} {DB_NAME}

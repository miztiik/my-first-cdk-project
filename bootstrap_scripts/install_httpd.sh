#!/bin/bash
sudo yum install -y httpd
sudo chkconfig httpd on
sudo service httpd start
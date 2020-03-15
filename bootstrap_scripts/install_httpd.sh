#!/bin/bash -xe

# Lets log everything to console for being lazy (not recommended)
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

sudo yum install -y httpd
ip=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
echo "<html><head><title>Modern Web App</title><style>body {margin-top: 40px;background-color: #333;}</style></head><body><div style=color:white;text-align:center><h1>Modern Web App</h1><p>Congratulations! Your Web Server is Online.</p></div></body></html>" >> /var/www/html/index.html
sudo chkconfig httpd on
sudo service httpd start
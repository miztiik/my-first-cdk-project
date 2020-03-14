#!/bin/bash
sudo yum install -y httpd
echo "<html><head><title>Modern Web App</title><style>body {margin-top: 40px;background-color: #333;}</style></head><body><div style=color:white;text-align:center><h1>Modern Web App</h1><p>Congratulations! Your Web Server is Online.</p></div></body></html>" >> /var/www/html/index.html
sudo chkconfig httpd on
sudo service httpd start
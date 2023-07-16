#!/usr/bin/env bash
# Script that sets up web servers for deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/releases/test/ # -p create parent dir
sudo mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

# append to nginx config file the ffg in server block section using alias
# to serve the content of data/.../current to hbtn_static
sudo sed -i '/listen 80 default_server/a location /hbtn_static { alias /data/web_static/current/;}' /etc/nginx/sites-available/default

sudo service nginx restart

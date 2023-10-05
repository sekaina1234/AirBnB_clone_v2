#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update -y
    apt-get install -y nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link and update ownership
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
if grep -q "location /hbnb_static {" "$config_file"; then
    sed -i '/location \/hbnb_static {/!b;n;c\        alias /data/web_static/current/;' "$config_file"
else
    echo "location /hbnb_static {
        alias /data/web_static/current/;
    }" >> "$config_file"
fi

# Restart Nginx
service nginx restart

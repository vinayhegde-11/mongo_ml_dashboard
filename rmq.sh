# Generated with the help of chatgpt

#!/bin/bash

# Update system packages
sudo apt update

# Install RabbitMQ and its dependencies
sudo apt install -y rabbitmq-server

# Enable and start RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Enable RabbitMQ management plugin
sudo rabbitmq-plugins enable rabbitmq_management

# Create user 'vinay' with password 'vinay'
sudo rabbitmqctl add_user vinay vinay

# Set 'vinay' as an administrator
sudo rabbitmqctl set_user_tags vinay administrator

# Create virtual host 'entries'
sudo rabbitmqctl add_vhost entries

# Set permission for 'vinay' to the virtual host 'entries'
sudo rabbitmqctl set_permissions -p entries vinay ".*" ".*" ".*"

# restart rabbitmq
sudo systemctl restart rabbitmq_server

# Display RabbitMQ status (optional)
sudo rabbitmqctl status

echo "RabbitMQ installation and setup complete!"
echo "RabbitMQ is running on port 5672, and management console is available at port 15672."
echo "Login to RabbitMQ management console with user 'vinay' and password 'vinay'."

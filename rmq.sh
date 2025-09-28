#!/bin/bash
# Usage: ./rmq.sh <username> <password>
# Example: ./rmq.sh myuser mypass

# Exit on error
set -e

# Check arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <username> <password>"
    exit 1
fi

RABBIT_USER=$1
RABBIT_PASS=$2

# Update system packages
sudo apt update

# Install RabbitMQ and its dependencies
sudo apt install -y rabbitmq-server

# Enable and start RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Enable RabbitMQ management plugin
sudo rabbitmq-plugins enable rabbitmq_management

# Create user with given username and password
sudo rabbitmqctl add_user "$RABBIT_USER" "$RABBIT_PASS" || true

# Set user as administrator
sudo rabbitmqctl set_user_tags "$RABBIT_USER" administrator

# Create virtual host 'entries'
sudo rabbitmqctl add_vhost entries || true

# Set permission for user to the virtual host 'entries'
sudo rabbitmqctl set_permissions -p entries "$RABBIT_USER" ".*" ".*" ".*"

# Restart RabbitMQ
sudo systemctl restart rabbitmq-server

# Display RabbitMQ status (optional)
sudo rabbitmqctl status

echo "===================================================="
echo "RabbitMQ installation and setup complete!"
echo "RabbitMQ is running on port 5672, and management console is available at port 15672."
echo "Login to RabbitMQ management console with:"
echo "   Username: $RABBIT_USER"
echo "   Password: $RABBIT_PASS"
echo "===================================================="

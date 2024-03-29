#!/bin/bash

# Create a copy of the environment variable file.
cp /opt/elasticbeanstalk/deployment/env /var/app/current/backend/.env

# Set permissions to the custom_env_var file so this file can be accessed 
# by any user on the instance. You can restrict permissions as per your requirements.
chmod 644 /var/app/current/backend/.env

# Remove duplicate files upon deployment.
# rm -f /opt/elasticbeanstalk/deployment/*.bak

# Source env vars
echo "source <(sed -E -n 's/[^\#]+/export &/ p'/var/app/current/backend/.env" >> ~/.bash_profile
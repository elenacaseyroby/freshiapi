# !/bin/bash

# Create a copy of the environment variable file.
cp /opt/elasticbeanstalk/deployment/env /opt/elasticbeanstalk/deployment/custom_env_var

# Set permissions to the custom_env_var file so this file can be accessed 
# by any user on the instance. You can restrict permissions as per your requirements.
chmod 644 /opt/elasticbeanstalk/deployment/custom_env_var

# Remove duplicate files upon deployment.
rm -f /opt/elasticbeanstalk/deployment/*.bak

# Set execution permissions on both .platform/hooks/postdeploy/01_set_env.sh. and 
# .platform/confighooks/postdeploy/01_set_env.sh files.
chmod +x .platform/hooks/postdeploy/01_set_env.sh
chmod +x .platform/confighooks/postdeploy/01_set_env.sh
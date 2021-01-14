#!/bin/bash
cd /var/app/staging/frontend
# Install node packages in frontend.
sudo npm install -y
# Create build files in frontend.
sudo npm run build -y
#!/usr/bin/env bash

# clean codedeploy-agent files for a fresh install
sudo rm -rf /root/install

# install CodeDeploy agent
sudo apt-get -y update
sudo apt-get -y install ruby
sudo apt-get -y install wget
cd /root
wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
sudo chmod +x ./install 
sudo ./install auto
wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf -

# update os & install python3
sudo apt-get update
sudo apt-get install -y python3 python3-dev python3-pip python3-venv python-is-python3 ffmpeg
# pip install --user --upgrade virtualenv

# delete app
sudo rm -rf /root/dj-localgovai-backend

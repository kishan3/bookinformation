#!/bin/bash


sudo apt-get update
sudo apt-get -y install python3
sudo apt install -y python3-pip
sudo apt-get install -y sqlite3 libsqlite3-dev

pip3 install virtualenv
virtualenv -p python3 venv

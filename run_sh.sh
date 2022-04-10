#!/bin/bash
apt install python3.8-venv -y
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
export SR_BOT_TOKEN=$1
export SR_DB_STRING=$2
python3 main.py
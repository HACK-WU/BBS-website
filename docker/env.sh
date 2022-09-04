#!/usr/bin/bash

mkdir -p /data/env/
mkdir /data/wwwroot/

set -eu
pip3 install virtualenv
pip3 install --upgrade pip; 
ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv3; 
cd /data/env/; 
virtualenv3 --python=/usr/bin/python3 bbs;
cd /data/env/bbs/bin/
source activate 
pip3 install django; 
pip3 install uwsgi; 
ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi; 
pip3 install pymysql; 
pip3 install pillow; 
pip3 install BeautifulSoup4 
set +e 
pip3 install -r /root/requirements.txt; 
set -e

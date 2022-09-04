#!/usr/bin/bash
set -eu
if [ -z  "$db_host" ];then
	echo "请指定数据库来连接地址"
	echo "-e db_host=remote_db_ip"
	exit
fi

source /data/env/bbs/bin/activate
sed -i   "s/\"HOST\":\"[0-9]\{3\}\..*\"/\"HOST\":\"$db_host\"/g" /data/wwwroot/BBS/BBS/settings.py
cd /data/wwwroot/BBS/
python3 manage.py runserver 0.0.0.0:80
if [ "$?" -ne 0  ];then
while :
do
	echo "hello"
	sleep 2
done 
fi

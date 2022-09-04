# BBS-website
这是一个利用Django搭建的，仿照博客园网站，编写的博客系统。 
目前大部分主体功能已经实现，还有少数部分功能没有实现。比如删除，和重新编辑文章的功能还没有编写完成。


## 准备数据库

* 创建登录用户

```sql
mysql > create user bbs@"%" identified by "123456"	#创建登录用户
mysql > grant all on *.* to bbs@"%" 				#授权
```

* 导入数据库

```sql
mysql > create database bbs;
.......
mysql bbs < bbs.sql -p
```

# docker 部署

* 上传BBS源码文件

```shell
mkdir /data/wwwroot/ -p		
cp BBS /data/wwwroot/			#拷贝BBS源码问价到此目录下
```

* 创建镜像并运行

```shell
docker build -f dockerfile_bbs -t bbs:v1 .			#创建镜像
docker run --name bbs -p 80:80 -e db_host=192.168.23.12 -v /data/wwwroot/:/data/wwwroot/ -d bbs:v1
	#db_host是数据库的ip地址
```



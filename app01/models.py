from django.db import models

# Create your models here.

'''
先写普通字段，
再写外键字段
'''
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):

        #verbose_naeme: 后台显示对应的名称
        #phone=models.BigIntegerField(verbose_name="手机号",null=True,blank=True)null=Ture:  数据库字段可以为空
        #blank=True: 后台管理字段可以为空
    avatar=models.FileField(upload_to="avatar/",default="avatar/default.png",verbose_name="用户头像")
    '''
    给avatar字段传文件对象，该文件会自动存储到avatar文件夹下，然后avatar字段只保存文件的路径avatar/default.png
        upload_to   :存储的路径位置
        default:    默认值
    '''
    create_time=models.DateField(auto_now_add=True)
    blog = models.OneToOneField(to="Blog",null=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural="用户表"   #修改admin后台管理默认的表名
    def __str__(self):
        return self.username

class Blog(models.Model):
    stie_name=models.CharField(verbose_name="站点名称",max_length=32)
    site_title=models.CharField(verbose_name="站点标题",max_length=32)
    site_theme=models.CharField(verbose_name="站点样式",max_length=64)
    #存储css/js文件的路径
    def __str__(self):
        return self.stie_name

class Category(models.Model):   #分类种类
    name=models.CharField(verbose_name="文章分类",max_length=32)
    blog=models.ForeignKey(to="Blog",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Tag(models.Model):    #标签
    name=models.CharField(verbose_name="文章标签",max_length=32)
    blog=models.ForeignKey(to="Blog",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Article(models.Model):    #文章
    title=models.CharField(verbose_name="文章标题",max_length=32)
    desc=models.CharField(verbose_name="文章简介",max_length=255)
    #文章内容分有很多，一般情况下都是使用TextField
    content=models.TextField(verbose_name="文章内容")
    create_time=models.DateField(auto_now_add=True)
    #数据库字段优化
    up_num=models.BigIntegerField(verbose_name="点赞数",default=0)
    down_num=models.BigIntegerField(verbose_name="点踩数",default=0)
    comment_num=models.BigIntegerField(verbose_name="评论数",default=0)

    #外键字段
    blog=models.ForeignKey(to="Blog",null=True,on_delete=models.CASCADE)
    category=models.ForeignKey(to="Category",null=True,on_delete=models.CASCADE)
    tags=models.ManyToManyField(to="Tag",through="Article2Tag",through_fields=("article","tag"))

    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    article=models.ForeignKey(to="Article",on_delete=models.CASCADE)
    tag=models.ForeignKey(to="Tag",on_delete=models.CASCADE)


class UpAndDown(models.Model):
    user=models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    article=models.ForeignKey(to="Article",on_delete=models.CASCADE)
    is_up=models.BooleanField()         #传布尔值 存0/1

class Comment(models.Model):
    user=models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    article=models.ForeignKey(to="Article",on_delete=models.CASCADE)
    content=models.CharField(verbose_name="评论内容",max_length=255)    #评论内容
    comment_time=models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    #自关联
    parent=models.ForeignKey(to="self",null=True,on_delete=models.CASCADE)

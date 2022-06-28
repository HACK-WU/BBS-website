"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$",views.home),
    #测试页面
    path("test/",views.test),
    re_path(r"^register/",views.register,name="reg"),
    re_path(r"^login/",views.login,name="login"),
    #图片验证码相关操作
    re_path(r"^get_code/",views.get_code,name="get_code"),
    #首页
    re_path(r"^home/",views.home,name="home"),
    #修改密码
    re_path(r"^set_password/",views.set_password,name="set_pwd"),
    #退出登录
    re_path(r"^logout/",views.logout,name="logout"),

    #暴露后端指定文件夹资源
    re_path(r"^media/(?P<path>.*)",serve,{"document_root":settings.MEDIA_ROOT}),

    #点赞点踩
    re_path(r"^up_or_down/",views.up_or_down),
    # 评论
    re_path(r"^comment/",views.comment),
    #个人站点页面搭建

    #后台管理
    re_path(r"^backend/",views.backend),
    #添加文章
    re_path(r"^add_article",views.add_article),
    #编辑器上传图片接口
    re_path(r"^upload_image/",views.upload_image),
    #修改用户头像
    re_path(r"^set_avatar/",views.set_avatar),

    re_path(r"^(?P<username>\w+)/$",views.site,name="site"),
    #侧边栏筛选
    re_path(r"^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/",views.site),

    #文章详情页
    re_path(r"^(?P<username>\w+)/article/(?P<article_id>\d+)/",views.article_detail),


]

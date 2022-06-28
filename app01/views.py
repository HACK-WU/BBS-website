from django.db.models.functions import TruncMonth
from django.shortcuts import render,HttpResponse,redirect
from app01.myforms import MyRegForm
from app01 import models
from django.http import JsonResponse
from django.contrib import  auth
from django.contrib.auth.decorators import login_required
import json
from django.db.models import F,Q
from app01.myModel import  myCaptcha


from django.db.models import  Count
from  django.core.paginator import Paginator,EmptyPage
# Create your views here.

def test(request):
    return render(request,"test.html")

def register(request):
    form_obj=MyRegForm()    #这是用于渲染前端标签以及检验数据的forms对象，
    if request.method=="POST":
        back_dic={"code":1000,"msg":""}
        '''
            back_dic字典是用于返回给前端的响应信息。初始内容为：
                code：1000   状态码，1000表示格式正确，意味告诉前端，数据校验是否通过
                msg:" "     报错信息，初始为空。
        '''
        form_obj=MyRegForm(request.POST)    #将数据传入forms对象。
        '''
            request.POST中存放的知识普通的键值对字符信息。所以不包含文件数据
            request.FILES中存放的就是二进制的文件信息，也是以键值对的形式
        '''
        #判断数据是否合法
        if form_obj.is_valid():
            '''
            froms.is_valid()  返回值是boolean,判断数据校验是否全都通过
                -全部通过返回True,否则返回False
                
                校验通过的数据，会被存放在forms.cleaned_data  对象中，这个对象是一个字典
                校验失败的数据，报错信息会被存放在forms.errors 对象中，这个对象是一个序列
            '''

            # {'username': 'hack', 'password': '123', 'confirm_password': '123', 'email': '123@qq.com'}
            cleaned_data=form_obj.cleaned_data  #将校验通过的数据字典赋值给一个变量
            #将字典里面的confirm_password键值对删除
            cleaned_data.pop("confirm_password")
            # {'username': 'hack', 'password': '123', 'email': '123@qq.com'}
            #用户头像
            file_obj=request.FILES.get("avatar")
            '''
            针对用户头像，一定要判断是否传值，不能直接添加到字典里面
            '''
            if file_obj:
                print("获取到头像！！")
                cleaned_data["avatar"]=file_obj
            #直接操作数据库，保存数据
            models.UserInfo.objects.create_user(**cleaned_data)
            back_dic["url"]="/login/"   #数据校验通过，告诉前端通过了之后，页面跳转的地址。
            print(form_obj.cleaned_data)
            return JsonResponse(back_dic)   #返回一个josn数据类型给前端
        else:
            back_dic["code"]=2000   #code：2000，表示校验失败的状态码
            back_dic["msg"]=form_obj.errors     #全局报错信息，里面可以封装所有的字段的报错信息。
            return JsonResponse(back_dic)
    return render(request,"register.html",locals())

'''
    ****************************************登录验证**************************************
'''
def login(request):
    if request.method=="POST":
        back_dic={"code":1000,"msg":""}
        username=request.POST.get("username")
        password=request.POST.get("password")
        code=request.POST.get("id_code")
        #1、先检验验证码是否正确
        # if request.session.get("code").upper()==code.upper():  #统一转大写，比较
        if myCaptcha.check_captcha(request,code):
            #2、校验用户名和密码是否正确
            user_obj=auth.authenticate(request,username=username,password=password)
            #验证通过是一个用户对象，不通过返回None
            if user_obj:
                #保存用户状态
                auth.login(request,user_obj)
                back_dic["url"]="/home/"
            else:
                back_dic["code"]=2000
                back_dic["msg"]="用户名或密码错误"
        else:
            back_dic["code"]=3000
            back_dic["msg"]="验证码错误"
        return JsonResponse(back_dic)
    return render(request,"login.html")


'''
    **********************************产生图片验证码***************************************
'''

'''
    图片相关的模块
        pip install pillow
        
'''
from PIL import Image,ImageDraw,ImageFont
'''
    Image:生成图片
    ImageDraw:能够在图片上乱涂乱画
    ImageFont；用来控制字体样式
    
'''
from io import BytesIO,StringIO
'''
   内存管理器模块
   BytesIO: 临时帮你存储数据，返回的时候，数据是二进制格式
   StringIO:临时帮你存储数据，返回使的时候，数据是字符串
    
'''
def get_code(request):
    io_obj=myCaptcha.get_captcha(request)     #获得一个验证码图片对象
    return HttpResponse(io_obj)

'''
    ******************************搭建首页****************************************
'''
from app01.MyClassObject import MyPaginator
def home(request):
    #查询本网站的所有的文章数据展示到前端页面，这里可以使用分页器
    article_query_set=models.Article.objects.all()
    myPaginator=MyPaginator()
    dic=myPaginator.createPages(request,article_query_set,3)
    locals().update(dic)
    return render(request,"home.html",locals())

@login_required()
def set_password(request):
    if True:
        back_dic={"code":1000,"msg":""}
        if request.method=="POST":
            old_password=request.POST.get("old_password")
            new_password=request.POST.get("new_password")
            confirm_password=request.POST.get("confirm_password")
            is_right=request.user.check_password(old_password)
            if is_right:
                if new_password==confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    back_dic["msg"]="密码修改成功"
                else:
                    back_dic["code"]=2000
                    back_dic["msg"]="两次密码不一致"
            else:
                back_dic["code"]=3000
                back_dic["msg"]="原密码错误"
        return JsonResponse(back_dic)
    return HttpResponse("set_pwd")


@login_required()
def logout(request):
    auth.logout(request)
    return redirect("/home/")





'''
    ****************************个人站点********************************
'''
def site(request,username,**kwargs):
    '''
        kwargs :如果该参数有值，也就意味着，需要对article_list做额外的筛选操作
    '''
    #先校验当前用户名是否存在
    user_obj=models.UserInfo.objects.filter(username=username).first()
    #用户名如果不存在返回一个404页面
    if not user_obj:
        return render(request,"errors.html")
    blog=user_obj.blog
    #查询当前个人站点下的所有文章
    article_list=models.Article.objects.filter(blog=blog)
    if kwargs:
        print(kwargs)
        condition=kwargs.get("condition")
        param=kwargs.get("param")
        #判断用户到底想按照哪个条件筛选数据
        if condition=="category":
            article_list=article_list.filter(category_id=param)
        elif condition=="tag":
            article_list=article_list.filter(tags__id=param)
        else:
            year,month=param.split("-") #2022-11 [2022,11]
            article_list=article_list.filter(create_time__year=year,create_time__month=month)

    return render(request,"site.html",locals())

def article_detail(request,username,article_id):
    user_obj=models.UserInfo.objects.get(username=username)
    blog=user_obj.blog
    #先获取文章对象
    article_obj=models.Article.objects.get(pk=article_id,blog__userinfo__username=username)
    if not article_obj:
        return render(request,"errors.html")
    #获取当前文章所有的评论内容
    comment_list=models.Comment.objects.filter(article=article_obj)

    return render(request,"article_detail.html",locals())

#点赞点踩
def up_or_down(request):
    '''
        1、校验当前用户是否登录
        2、判断当前文章是否是当前用户自己写的（用户不可以给自己文章点赞点踩）
        3、判断当前用户是否已经给当前文章点过了。只能点一次。
        4、操纵数据库
    '''
    if request.method=="POST":
        back_dic={
            "code":1000,
            "msg":"",
        }
        #1、判断当前用户是否登录
        if request.user.is_authenticated:     #用户已经登录
            article_id=request.POST.get("article_id") #文章主键值
            isUp=request.POST.get("isUp")   #返回值是一个字符串，值是"true"或者"false"
            isUp=json.loads(isUp)           #将普通字符串，转换为python格式的数据类型，相当于去掉双引号操作
            #2、判断当前文章是否是当前用户自己写的。
            article_obj=models.Article.objects.get(pk=article_id)
            if not article_obj.blog.userinfo==request.user:
                #3、校验当前用户是否已经点了
                is_click=models.UpAndDown.objects.filter(user=request.user,article=article_obj)
                if not is_click:
                    #4、操作数据库，纪录数据 要同步操作普通字段
                    # 判断当前用户是点了赞还是踩 从而决定给哪个字段加一
                    if isUp:
                        #给点赞数加一
                        models.Article.objects.filter(pk=article_id).update(up_num=F("up_num")+1)
                        back_dic["msg"]="点赞成功"
                    else:
                        #给点踩数加一
                        models.Article.objects.filter(pk=article_id).update(down_num=F("down_num")+1)
                        back_dic["msg"]="点踩成功"
                    # 操作点赞点踩表
                    models.UpAndDown.objects.create(user=request.user,article=article_obj,is_up=isUp)
                else:
                    back_dic["code"]=2000
                    back_dic["msg"]="你已经点过了，不能在点了"
            else:
                back_dic["code"]=3000
                back_dic["msg"]="不能给自己点赞"
        else:
            back_dic["code"]=4000
            back_dic["msg"]="<p><a href='/login/'>请先登录</a></p>"
        print("*********执行完毕*************")
        return JsonResponse(back_dic)

from django.db  import transaction
def comment(request):
    #自己可以评论自己的文章
    if request.method=="POST":
        back_dic={"code":1000,"msg":""}
        if request.user.is_authenticated:
            article_id=request.POST.get("article_id")
            content=request.POST.get("content")
            parent_id=request.POST.get("parent_id")
            #直接操作评论表存储数据  两张表
            with transaction.atomic():
                models.Article.objects.filter(pk=article_id).update(comment_num=F("comment_num")+1)
                models.Comment.objects.create(user=request.user,article_id=article_id,content=content,parent_id=parent_id)
                back_dic["msg"]="评论成功"
        else:
            back_dic["code"]=2000
            back_dic["msg"]="未登录"
        return JsonResponse(back_dic)


'''
    *********************后台管理啊**************************
'''
from bs4 import BeautifulSoup
@login_required()
def backend(request):
    article_list=models.Article.objects.filter(blog=request.user.blog)  #查询当前用户所有的文章
    myPaginator=MyPaginator()
    dic=myPaginator.createPages(request,article_list,2)
    locals().update(dic)
    return render(request,"backend/backend.html",locals())

@login_required()
def add_article(request):   #添加文章
    if request.method=="POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        category_id=request.POST.get("category")
        tag_id_list=request.POST.getlist("tag")
        #模块使用
        #1、先生成一个对象
        soup=BeautifulSoup(content,"html.parser")
        #2、获取所有的标签
        tags=soup.find_all()
        for tag in tags:
            # print(tag.name) #获取所有的标签名
            # 针对scrip标签直接删除
            if tag.name=="script":
                #删除标签
                tag.decompose()
        #文章简介
        #1、先简单暴力的直接切去content 150个字符
        # desc=content[0:150]
        #2、截取文本150个字符
        desc=soup.text[0:150]
        article_obj=models.Article.objects.create(
            title=title,
            content=str(soup),
            desc=desc,
            category_id=category_id,
            blog=request.user.blog
        )
        #文章和标签的关系表 是我们自己创建的，无法使用add set remove clear 方法
        #自己去操作关系表 一次性可能需要创建多条数据 批量插入bulk_create()
        article_obj_list=[]
        for i in tag_id_list:
            tag_article_id=models.Article2Tag(article=article_obj,tag_id=i)
            article_obj_list.append(tag_article_id)
        #批量插入数据
        models.Article2Tag.objects.bulk_create(article_obj_list)
        # 跳转到后台管理文章的展示页
        return redirect("/backend/")
    category_list=models.Category.objects.filter(blog=request.user.blog)#当前用户文章的所有的分类
    tag_list=models.Tag.objects.filter(blog=request.user.blog)
    return render(request,"backend/add_article.html",locals())


import os
from BBS import  settings
def upload_image(request):
    '''
    //成功时
{
        "error" : 0,
        "url" : "http://www.example.com/path/to/file.ext"
}
//失败时
{
        "error" : 1,
        "message" : "错误信息"
}

    '''
    #用户写文章上传的图片，也算静态资源 应该放到media文件夹下
    if request.method=="POST":
        back_dic={"error":0} #先提前定义返回给编辑器的数据格式
        #获取用户上传的图片对象
        print(request.FILES)      #打印，查看file对象的key
        file_obj=request.FILES.get("imgFile")
        #手动拼接存储路径文件的路径
        file_dir=os.path.join(settings.BASE_DIR,"media","article_img")
        #优化操作，先判断当前文件夹是否存在， 不存在，自动创建
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)  #创建一层目录结构 article_img
        #拼接图片的完整路径
        file_path=os.path.join(file_dir,file_obj.name)
        print(file_path)
        with open(file_path,"wb") as f:
           for line in file_obj:
               f.write(line)
        #为什么不直接使用file_path
        back_dic["url"]=f"media/article_img/{file_obj.name}"
        print("执行完毕")
        return JsonResponse(back_dic)

@login_required()
def set_avatar(request):
    blog=request.user.blog
    username=request.user.username
    if request.method=="POST":
        file_obj=request.FILES.get("avatar")
        # models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=file_obj)  #不会再自动加avatar
        #利用对象的属性，做数据库更新
        user_obj=request.user
        user_obj.avatar=file_obj
        user_obj.save()
        return redirect("/home/")
    return render(request,"backend/set_avatar.html",locals())


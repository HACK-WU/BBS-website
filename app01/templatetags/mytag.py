# _*_ coding : utf-8 _*_
# @Time : 2022/5/8 16:37
# @Author : HackWu
# @File : mytag
# @Project : BBS

from django import template
from django.db.models.functions import TruncMonth

from app01 import models
from django.db.models import  Count
register=template.Library()

#自定义inclusion_tag
@register.inclusion_tag("mytemplates/left_menu.html")
def left_menu(username):
    user_obj=models.UserInfo.objects.filter(username=username).first()
    blog=user_obj.blog
    #构造侧边栏需要的数据
    #1、查询当前用户所有的分类，及分类下的文章数
    category_list=models.Category.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list("name","count_num","pk")
    # print(category_list)
    #2、查询当前用户所有的标签以及标签下的文章数
    tag_list=models.Tag.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list("name","count_num","pk")
    # print(tag_list)
    #3、按照年月统计所有文章
    date_list=models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("create_time")).values("month").annotate(count_num=Count("pk")).values_list("month","count_num")
    # print(date_list)
    return locals()

@register.inclusion_tag("mytemplates/test2.html")
def test():
    return locals()




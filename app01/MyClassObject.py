# _*_ coding : utf-8 _*_
# @Time : 2022/5/8 17:51
# @Author : HackWu
# @File : MyClassObject
# @Project : BBS
from django.core.paginator import Paginator, EmptyPage
class MyPaginator():
    def __init__(self):
        self.page_range=None
        self.current_page=None
        self.num=None
    def createPages(self,request,queryset_obj,content_num=3):
        num=request.GET.get("page")
        if not num: #如果num为空
            num="1"
        num=int(num)
        paginator=Paginator(queryset_obj,content_num)
        self.page_range=paginator.page_range  #获取到分页范围
        if paginator.num_pages>11:
            right=num+6
            left=num-5
            if right>paginator.num_pages:
                right=paginator.num_pages
            if left<=0:
                left=1
            self.page_range=range(left,right)
        try:
            self.current_page=paginator.page(num)    #获取到当前的分页内容
        except EmptyPage as  e:
            self.current_page=paginator.page(1)      #如果出错默认显示第一页的内容
        self.num=num
        dic={
            "current_page":self.current_page,
            "page_range":self.page_range,
            "num":self.num
        }
        return dic   #返回当前页面和页面的范围


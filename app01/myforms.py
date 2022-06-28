# _*_ coding : utf-8 _*_
# @Time : 2022/5/4 14:30
# @Author : HackWu
# @File : myforms
# @Project : BBS

from django import forms
from app01 import models
from django.core.exceptions import ValidationError
class MyRegForm(forms.Form):
    username=forms.CharField(label="用户名",min_length=3,max_length=8,
                             error_messages={
                                 "required":"用户名不能为空",
                                 "min_length":"用户名最少3位",
                                 "max_length":"用户名最多8位"
                             },
                             #还需要让标签有bootstrap样式
                             widget=forms.widgets.TextInput(attrs={"class":"form-control"})
                             )
    password=forms.CharField(label="密码",min_length=3,
                             error_messages={
                                 "required":"密码不能为空",
                                 "min_length":"密码最少3位",
                             },
                             #还需要让标签有bootstrap样式
                             widget=forms.widgets.PasswordInput(attrs={"class":"form-control"}))
    confirm_password=forms.CharField(label="确认密码",min_length=3,
                                     error_messages={
                                         "required":"密码不能为空",
                                         "min_length":"密码最少3位",
                                     },
                                     #还需要让标签有bootstrap样式
                                     widget=forms.widgets.PasswordInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="邮箱",
                           error_messages={
                             "required":"邮箱不能为空",
                               "invalid":"邮箱格式不正确",
                           },
                           widget=forms.widgets.EmailInput(attrs={"class":"form-control"})
                            )


    def clean_username(self):
        username=self.cleaned_data.get("username")
        #去数据库中校验
        is_exists=models.UserInfo.objects.filter(username=username)
        if is_exists:
            #提示信息
           raise ValidationError("用户名已存在")
        return username

    #全局钩子
    def clean(self):
        password=self.cleaned_data.get("password")
        confirm_password=self.cleaned_data.get("confirm_password")
        if not password==confirm_password:
            raise ValidationError("false")
        return self.cleaned_data
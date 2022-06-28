# _*_ coding : utf-8 _*_
# @Time : 2022/5/10 22:20
# @Author : HackWu
# @File : mySettings
# @Project : BBS


#验证码图片设置
set_captcha={
    "ignore_case":"True",                   #是否忽略大小写,True表示忽略
    "use_system_image":"True",              #是否使用系统图片，True为是，如果为False，需要给定自己的图片路径
    "image_url":"static/img/qq.png",        #图片路径，如果use_system_image=False时，必须填写
    "image_format":"png",                   #图片格式
    "image_size":(430,35),                  #图片大小，如果是自己的图片，图片的大小，必须和这个保持一致
    "font_size":30,                         #字体大小
    "font_url":"static/font/simsun.ttf",    #字体的路径，是一个tff文件
}
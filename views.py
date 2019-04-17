from django.http import HttpResponse
import json
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
import os
from django.conf import settings
from firm.models import *
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
from firm.myLogger import LogHelper
from firm.pdf_to_txt_class import ParsePDFtoTXT

# Create your views here.


# 装饰器函数(判断用户是否在登陆状态)
def login_decorator(func):
    """此方法为装饰器，用来判定用户是否在登录状态"""
    def login_func(request, *args, **kwargs):
        if request.session.get("uname"):
            return func(request, *args, **kwargs)
        else:
            resp = redirect("/login")
            resp.set_cookie("url", request.path)
            return resp
    return login_func


# 加密解密方式
auth_check = "MarcelArhut"


# 首页展示页面
def index_views(request):
    uname = request.session.get("uname", "")
    print(uname)
    if uname == "":
        message = "未登录"
    else:
        message = "欢迎" + uname
    # return HttpResponse("欢迎来到我的首页")
    return render(request, 'index.html', locals())


# 用户登陆页面
def login_views(request):
    uname = request.session.get("uname", "")
    print(uname)
    if uname == "":
        message = "未登录"
    else:
        message = "欢迎" + uname
    if request.method == "GET":
        if "uname" in request.session:
            uname = request.session.get("uname")
            return redirect('/', {"message": uname})
        if "uname" in request.COOKIES:
            uname = request.COOKIES.get("uname")
            request.session['uname'] = uname
            return redirect('/', {"message": uname})
        return render(request, 'login.html', locals())
    elif request.method == "POST":
        # errMsg = {"message": "用户名或密码错误"}
        uname = request.POST.get("uname")
        check_user_list = UserInfo.user_obj.filter(uname=uname)
        code_info = request.session.get("code_show", "")
        print("session里的code:", code_info)
        code_check = request.POST.get("code_check")
        if not check_user_list:
            return render(request, 'login.html', {"message_name": "用户名或密码错误"})
        if code_info.upper() != code_check.upper():
            # code_show = {"message": "验证码错误"}
            return render(request, 'login.html', {"message_code": "验证码错误"})
        upwd = check_password(request.POST.get("upwd"), check_user_list[0].upwd)
        if upwd:
            print("登录成功了")
            request.session['uname'] = uname
            return redirect('/')
            # if "rember_upwd" in request.POST:
            #     print("记住密码了哦")
            #     request.COOKIES['uname'] = uname
            #     return redirect('/shop/')
            # else:
            #     print("未记住密码哈")
            #     return redirect('/shop/')
        else:
            # errMsg = {"message": "用户名或密码错误"}
            return render(request, 'login.html', {"message_name": "用户名或密码错误"})


# 用户注册页面
def register_views(request):
    uname = request.session.get("uname", "")
    print(uname)
    if uname == "":
        message = "未登录"
    else:
        message = "欢迎" + uname
    if request.method == "GET":
        return render(request, 'register.html', locals())
    elif request.method == "POST":
        print(request.method)
        print("post请求")
        uname = request.POST.get("uname")
        upwd = make_password(request.POST.get("upwd"), auth_check, "pbkdf2_sha1")
        cpwd = request.POST.get("cpwd")
        uphone = request.POST.get("uphone")
        uemail = request.POST.get("uemail")
        user_uname_querySet = UserInfo.user_obj.filter(uname=uname)
        user_uphone_querySet = UserInfo.user_obj.filter(uphone=uphone)
        user_uemail_querySset = UserInfo.user_obj.filter(uemail=uemail)
        if uname == "":
            return render(request, 'register.html', {"message_uname": "null"})
        elif len(uname) <= 3:
            return render(request, 'register.html', {"message_uname": "gt3"})
        elif user_uname_querySet:
            return render(request, 'register.html', {"message_uname": "exist"})
        elif request.POST.get("upwd") == "":
            return render(request, 'register.html', {"message_upwd_null": "密码不能为空"})
        elif request.POST.get("upwd") != cpwd:
            return render(request, 'register.html', {"message_cpwd_diff": "密码输入不一致"})
        elif uphone == "":
            return render(request, 'register.html', {"message_uphone": "null"})
        elif uphone[0] != "1" or len(uphone) != 11:
            return render(request, 'register.html', {"message_uphone": "not_allow"})
        elif user_uphone_querySet:
            return render(request, 'register.html', {"message_uphone": "exist"})
        elif uemail == "":
            return render(request, 'register.html', {"message_uemail": "null"})
        elif (uemail[0] == "@") or ("@" not in uemail) or (uemail[-4:] != ".com"):
            return render(request, 'register.html', {"message_uemail": "not_allow"})
        elif user_uemail_querySset:
            return render(request, 'register.html', {"message_uemail": "exist"})
        print("开始注册")
        UserInfo.user_obj.create(uname=uname, upwd=upwd, uphone=uphone, uemail=uemail)
        request.session['uname'] = uname
        request.session.set_expiry(0)
        print("注册成功")
        return redirect('/')

@login_decorator
def pdf_to_txt_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    if request.method == "GET":
        return render(request, 'pdf_to_txt.html', locals())
    elif request.method == "POST":
        src_pdf_path = request.POST.get("pdf_path")
        save_txt_path = request.POST.get("txt_path")
        if not os.path.exists(save_txt_path):
            os.makedirs(save_txt_path)
        if not os.path.exists(src_pdf_path):
            return render(request, 'pdf_to_txt.html', {"pdf_info": "pdf原路径异常"})
        else:
            parse = ParsePDFtoTXT(src_pdf_path, save_txt_path)
            dic = parse.parse_pdf2txt()
            # json_str = json.dump(result)
            return render(request, 'pdf_to_txt.html', locals())

@login_decorator
def txt_to_csv_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    return render(request, 'txt_to_csv.html', locals())

@login_decorator
def sort_csv_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    return HttpResponse("csv文件整理页面")

@login_decorator
def database_to_csv_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    return HttpResponse("将数据库数据导出csv页面")

@login_decorator
def query_data_views(request, page_num):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    if request.method == "GET":
        # 所有查询结果集
        data_obj_ls = JournalInfo.journal_obj.all()
        # 首页
        first_page_num = 1
        # 每页展示数量
        show_num = 15
        if page_num < 1:
            page_num = 1
        # 下一页
        next_page = page_num + 1
        if not data_obj_ls[next_page*show_num:(next_page+1)*show_num]:
            next_page = page_num
        # 上一页
        before_page = page_num - 1
        if before_page < 1:
            before_page = 1
        if len(data_obj_ls) % show_num == 0:
            page_count = len(data_obj_ls) // show_num
        else:
            page_count = len(data_obj_ls) // show_num + 1
        # 尾页
        last_page = page_count - 1
        query_data_obj_ls = data_obj_ls[page_num*show_num:(page_num+1)*show_num]
        return render(request, 'query_data.html', locals())
    elif request.method == "POST":
        pass

@login_decorator
def upload_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    return render(request, 'upload.html', locals())


def code_create_views(request):
    # #图像的尺寸处理
    # #打开一个jpg图像文件,注意路径
    # image=Image.open('/home/tarena/qq.jpg')
    # #获得图像的尺寸
    # width,height=image.size
    # print('original image size:%sx%s'% (width,height))
    # #图像的缩放
    # image.thumbnail((width//2,height//2))
    # print('current image size:%sx%s'% (width//2,height//2))
    # #把缩放后的图像用jpeg格式保存:
    # image.save('thumbnail.jpg','jpeg')

    # #图像的模糊处理
    # #打开一个jpg图像文件,注意路径:
    # image=Image.open('/home/tarena/qq.jpg')
    # #应用模糊滤镜
    # filter_image=image.filter(ImageFilter.BLUR)
    # filter_image.save('blur.jpg','jpeg')

    # 验证码的制作

    # 随机字母
    def randomChar():
        return chr(random.randint(65, 90))

    # 图片背景随机颜色

    def randomBgColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 字体随机颜色

    def randomFontColor():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127),)

    # 创建图片大小240x60
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象
    font = ImageFont.truetype('arial.ttf', 36)

    # 创建Draw对象,实现图像的绘制
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=randomBgColor())
    # 输出文字
    code_txt_ls = []
    for t in range(4):
        create_str = randomChar()
        code_txt_ls.append(create_str)
        draw.text((60 * t + 10, 10), create_str, font=font, fill=randomFontColor())
    code_text = "".join(code_txt_ls)
    print("生产验证码是:", code_text)
    request.session['code_show'] = code_text
    # 模糊处理
    image = image.filter(ImageFilter.BLUR)
    # 释放画笔
    del draw
    #内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为jpeg
    image.save(buf, 'jpeg')
    return HttpResponse(buf.getvalue(), 'image/jpeg')
    # image.save('code.jpg', 'jpeg')


# 退出登陆状态
def logout_views(request):
    logout(request)
    return redirect('/')

def feedback_views(request):
    uname = request.session.get("uname", "")
    message = "欢迎" + uname
    return render(request, 'feedback.html', locals())


# 用户注册AJAX请求处理视图
def check_register_views(request):
    check_type = request.POST.get("check_type")
    print(check_type)
    if check_type == "uname":
        uname = request.POST.get("uname")
        user_list = UserInfo.user_obj.filter(uname=uname)
        if user_list:
            dic = {
                "flage": "1",
            }
        else:
            dic = {
                "flage": "0",
            }
        jsonStr = json.dumps(dic)
        print(jsonStr)
        print(type(jsonStr))
        return HttpResponse(jsonStr)
    elif check_type == "uphone":
        uphone = request.POST.get("uphone")
        user_list = UserInfo.user_obj.filter(uphone=uphone)
        if user_list:
            dic = {
                "flage": "1",
            }
        else:
            dic = {
                "flage": "0",
            }
        jsonStr = json.dumps(dic)
        return HttpResponse(jsonStr)
    elif check_type == "uemail":
        uemail = request.POST.get("uemail")
        user_list = UserInfo.user_obj.filter(uemail=uemail)
        if user_list:
            dic = {
                "flage": "1",
            }
        else:
            dic = {
                "flage": "0",
            }
        jsonStr = json.dumps(dic)
        return HttpResponse(jsonStr)

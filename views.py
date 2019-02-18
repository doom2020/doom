import json
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from shop.models import *
# Create your views here.

#加密解密方式
auth_check = "MarcelArhut"

def login_decorator(func):
    """此方法为装饰器，用来判定用户是否在登录状态"""
    def login_func(request, *args, **kwargs):
        if request.session.get("uname"):
            return func(request, *args, **kwargs)
        else:
            resp = redirect("/shop/login/")
            resp.set_cookie("url", request.path)
            return resp
    return login_func

#主页视图处理(可优化)
def main_views(request):
    return render(request, 'main.html', locals())

#公司文化展示视图处理pass掉了
def firm_show_views(request):
    return render(request, 'firm_show.html', locals())

#合作视图处理暂时pass掉了
def cooperation_views(request):
    return render(request, 'cooperation.html', locals())

#招聘视图处理暂时pass掉
@login_decorator
def employment_views(request):
    return render(request, 'employment.html', locals())

#官网客服视图处理暂时pass掉了
@login_decorator
def contact_me_views(request):
    return render(request, 'contact.html', locals())

#用户注册视图处理
def register_views(request):
    if request.method == "GET":
        return render(request, 'register_new.html', locals())
    elif request.method == "POST":
        print(request.method)
        print("post请求")
        uname = request.POST.get("uname")
        upwd = make_password(request.POST.get("upwd"), auth_check, "pbkdf2_sha1")
        cpwd = request.POST.get("cpwd")
        uphone = request.POST.get("uphone")
        uemail = request.POST.get("uemail")
        upicture = request.FILES.get("upicture")
        user_uname_querySet = UserInfo.objects.filter(uname=uname)
        user_uphone_querySet = UserInfo.objects.filter(uphone=uphone)
        user_uemail_querySset = UserInfo.objects.filter(uemail=uemail)
        if uname == "":
            return render(request, 'register_new.html', {"message_uname": "null"})
        elif len(uname) <= 3:
            return render(request, 'register_new.html', {"message_uname": "gt3"})
        elif user_uname_querySet:
            return render(request, 'register_new.html', {"message_uname": "exist"})
        elif request.POST.get("upwd") == "":
            return render(request, 'register_new.html', {"message_upwd_null": "密码不能为空"})
        elif request.POST.get("upwd") != cpwd:
            return render(request, 'register_new.html', {"message_cpwd_diff": "密码输入不一致"})
        elif uphone == "":
            return render(request, 'register_new.html', {"message_uphone": "null"})
        elif uphone[0] != "1" or len(uphone) != 11:
            return render(request, 'register_new.html', {"message_uphone": "not_allow"})
        elif user_uphone_querySet:
            return render(request, 'register_new.html', {"message_uphone": "exist"})
        elif uemail == "":
            return render(request, 'register_new.html', {"message_uemail": "null"})
        elif (uemail[0] == "@") or ("@" not in uemail) or (uemail[-4:] != ".com"):
            return render(request, 'register_new.html', {"message_uemail": "not_allow"})
        elif user_uemail_querySset:
            return render(request, 'register_new.html', {"message_uemail": "exist"})
        print("开始注册")
        UserInfo.objects.create(uname=uname, upwd=upwd, uphone=uphone, uemail=uemail, upicture=upicture)
        request.session['uname'] = uname
        request.session.set_expiry(0)
        print("注册成功")
        return redirect('/shop/')

#用户登录视图处理
def login_views(request):
    if request.method == "GET":
        if "uname" in request.session:
            uname = request.session.get("uname")
            return redirect('/shop/', {"message": uname})
        if "uname" in request.COOKIES:
            uname = request.COOKIES.get("uname")
            request.session['uname'] = uname
            return redirect('/shop/', {"message": uname})
        return render(request, 'login.html', locals())
    elif request.method == "POST":
        errMsg = {"message": "用户名或密码错误"}
        uname = request.POST.get("uname")
        check_user_list = UserInfo.objects.filter(uname=uname)
        if not check_user_list:
            return render(request, 'login.html', locals())
        upwd = check_password(request.POST.get("upwd"), check_user_list[0].upwd)
        if upwd:
            print("登录成功了")
            request.session['uname'] = uname
            if "rember_upwd" in request.POST:
                print("记住密码了哦")
                request.COOKIES['uname'] = uname
                return redirect('/shop/')
            else:
                print("未记住密码哈")
                return redirect('/shop/')
        else:
            return render(request, 'login.html', locals())

#取消登录视图处理
def logout_views(request):
    """此方法为取消登录状态，清除session,cookie"""
    auth.logout(request)
    return redirect("/shop")

#商品展示视图处理(页面显示逻辑可优化)
@login_decorator
def goods_detail_views(request, gtype, page):
    print(gtype)
    print(page)
    dic = {"gtype": gtype}
    gtype_obj = GoodsType.objects.get(id=gtype)
    #上一页
    if int(page) <= 1:
        before_page = int(page)
    else:
        before_page = int(page) - 1
    #下一页
    next_page = int(page) + 1
    #每页显示商品的数量为12个
    show_count = 12
    #第一页为1
    first_page = 1
    #第page页显示的商品为
    goods_list_all = gtype_obj.goods_set.all()[(page-1)*show_count:page*show_count]
    goods_list = goods_list_all
    # display_goods_list = goods_list[0:13]
    last_goods_count = len(goods_list) % 4
    count = 0
    goods_obj_all_list = []
    goods_obj_list = []
    for goods_obj in goods_list:
        goods_obj_list.append(goods_obj)
        count += 1
        if count % 4 == 0:
            goods_obj_all_list.append(goods_obj_list)
            goods_obj_list = []
    goods_obj_all_list.append(list(reversed(goods_list))[0:last_goods_count])
    print(goods_obj_all_list)
    return render(request, 'goods_detail.html', locals())

#商品的详细信息
@login_decorator
def goods_detail_one_views(request, goods_name):
    print(goods_name)
    goods_obj = Goods.objects.get(gname=goods_name)
    print(goods_obj.gpicture)
    return render(request, 'goods_detail_one.html', locals())

#购物车商品的添加ajax请求处理
def update_shopping_car_views(request):
    gname = request.POST.get("gname")
    gprice = request.POST.get("gprice")
    gcount = request.POST.get("gcount")
    user_name = request.session.get("uname")
    #通过用户名查询购物车
    user_obj = UserInfo.objects.get(uname=user_name)
    print("购买的用户对象：", user_obj)
    shopping_car_obj = ShoppingCar.objects.filter(userinfo=user_obj)
    #通过购物车对象查询购物车的所有商品
    goods_obj_list = []
    #如果该商品存在,数量则加一
    if goods_obj_list:
        print("商品存在哟")
        gcount = goods_obj_list.gcount + gcount
        goods_obj = ShoppingCar.objects.get(gname=gname, userinfo=user_obj)
        goods_obj.gcount = gcount
        goods_obj.save()
        print("商品数量更新成功")
    #如果该商品不存在，则添加入购物车
    else:
        print("商品不存在哦")
        # ShoppingCar.objects.create(gname=gname, gcount=gcount, userinfo=user_obj)
        print("添加购物车成功")
    dic = {
        "flage": "1",
    }
    jsonStr = json.dumps(dic)
    return HttpResponse(jsonStr)


#订单视图处理
@login_decorator
def order_views(request):
    return render(request, 'order.html', locals())

#显示用户信息
@login_decorator
def user_info_views(request):
    return render(request, 'user_info.html', locals())

#用户信息更改
@login_decorator
def update_user_info_views(request):
    pass

#增加收件人视图处理
@login_decorator
def add_address_views(request):
    if request.method == "GET":
        return render(request, 'address.html', locals())
    elif request.method == "POST":
        uname = request.POST.get("uname")
        uphone = request.POST.get("uphone")
        uaddress = request.POST.get("uaddress")
        user_name = request.session['uname']
        #通过买主的对象进行关联
        user_obj = UserInfo.objects.get(uname=user_name)
        print(uname, uphone, uaddress, user_name, user_obj)
        Address.objects.create(take_name=uname, take_phone=uphone, address_name=uaddress, userinfo=user_obj)
        return redirect('/shop/')

#取件人信息ajax请求处理暂无需处理
def check_address_views(request):
    pass

#用户注册信息ajax请求处理
def check_register_views(request):
    choose = request.POST.get("choose")
    print(choose)
    if choose == "uname":
        uname = request.POST.get("uname")
        user_list = UserInfo.objects.filter(uname=uname)
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
    elif choose == "uphone":
        uphone = request.POST.get("uphone")
        user_list = UserInfo.objects.filter(uphone=uphone)
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
    elif choose == "uemail":
        uemail = request.POST.get("uemail")
        user_list = UserInfo.objects.filter(uemail=uemail)
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
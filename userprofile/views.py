from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .forms import UserLoginForm,UserRegisterForm

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # clean_data 清洗出合法数据
            data = user_login_form.cleaned_data
            #检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username = data['username'],password = data['password'])
            if user:
                # 将用户数据保存在session中，即实现登录动作
                login(request,user)
                return redirect('article:article_list')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            return HttpResponse('用户名或密码输入不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context={'user_login_form':user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse('请使用GET或者POST请求')

def user_logout(request):
    #用户退出
    logout(request)
    return redirect('article:article_list')

def user_register(request):
    if request.method =="POST":
        user_register_form = UserRegisterForm(data=request.POST)
        print(user_register_form.is_valid())
        error = user_register_form.errors
        print(user_register_form.errors)
        print(str(user_register_form['username']))
        print(str(user_register_form['password1']))
        print(str(user_register_form['password2']))
        if user_register_form.is_valid():
            # 直接保存，并赋值给new_user
            new_user = user_register_form.save()
            login(request,new_user)
            return redirect('article:article_list')
        else:
            #输入密码不规范都会被检测为invalid，而不仅仅是密码不相同
            return render(request, 'userprofile/error.html',context={'error':error})
    # 如果get方法访问，也就是第一次进入页面：
    elif request.method == "GET":
        # 传入一个空表单
        user_register_form = UserRegisterForm()
        # 传入上下文并生成页面
        context={'form':user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("请使用GET或者POST请求")

# @login_required是一个Python装饰器。装饰器可以在不改变某个函数内容的前提下，给这个函数添加一些功能。
# 具体来说就是@login_required要求调用user_delete()函数时，用户必须登录；
# 如果未登录则不执行函数，将页面重定向到/userprofile/login/地址去。
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            #退出登录，删除数据并返回博客列表
            logout(request)
            # 装饰器确定用户登录后，允许调用user_delete().
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


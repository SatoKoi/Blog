import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from utils.common import MSG_DICT
from utils.email_send import send_register_email, generate_random_code

from .models import UserProfile, EmailVarifyRecord
from .forms import LoginForm, RegisterForm, ResetPwdForm, ForgetPwdForm
from django.contrib.auth.backends import ModelBackend


class CustomBackend(ModelBackend):
    """自定义帐号认证方法"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # user = UserProfile.objects.get(username=username)   # 此处为and级用法, 但业务逻辑应该为or级操作
            # (username=username or email=username) and password=password 认证逻辑
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 将明文加密, 与存储在后台的密文进行比对
                return user
        except Exception:
            return None


class LoginView(View):
    """登录页面"""
    def get(self, request):
        # 如果用户已经登录, 跳转到后台管理页面
        if request.user.is_staff:
            return redirect(to='/xadmin/')

        if request.user.is_authenticated:
            redirect_url = request.GET.get('next', None)
            if redirect_url:
                return redirect(to=redirect_url)
            return redirect(to='/')
        # confirmed = request.COOKIES.get('confirm', 0)
        # if is_redirect and confirmed == 0:
        #     status = 'danger'       # danger 提示红色错误信息, info 提示蓝色正确信息
        #     msg = '操作需要登录'
            # response = render(request, "login.html", {"msg": msg, "status": status})
            # response.set_cookie('confirm', 1)
            # return response
        # 数据转发与清理
        next_url = request.GET.get('next', None)
        request.session.update({'next_url': next_url})
        msg = request.session.get('msg', None)
        status = request.session.get("status", None)
        if msg:
            del request.session['msg']
        if status:
            del request.session['status']
        if not msg:
            msg = request.GET.get("msg", "")
        if not status:
            status = request.GET.get("status", "")
        if msg in MSG_DICT.keys():
            msg = MSG_DICT.get(msg)
        return render(request, "login.html", {"msg": msg, "status": status})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(request, username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:          # 如果用户帐号已经激活
                    login(request, user)    # 登录账户
                    redirect_url = request.session.get('next_url')
                    if redirect_url:
                        del request.session['next_url']
                        return HttpResponse(json.dumps({"status": "success", "url": redirect_url}), content_type='application/json')
                    return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({"msg": "用户未激活! ", "status": "failure"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": "用户名或密码错误! ", "status": "failure"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"msg": "表单验证失败! ", "status": "failure"}), content_type='application/json')


class LogoutView(View):
    """注销"""
    def get(self, request):
        logout(request)
        return redirect(to='/')


class RegisterView(View):
    """注册页面"""
    def get(self, request):
        register_form = RegisterForm()          # 设置了captcha字段, 将验证码内容显示到前端
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            if UserProfile.objects.filter(email=email):
                return HttpResponse(json.dumps({"status": "failure", "msg": "邮箱已经存在"}), content_type="application/json")
            if UserProfile.objects.filter(username=user_name):
                return HttpResponse(json.dumps({"status": "failure", "msg": "用户名已经存在"}), content_type="application/json")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = False  # 表明用户尚未激活
            user_profile.password = make_password(pass_word)  # 对密码进行加密
            user_profile.save()             # 保存数据到用户数据库

            token = send_register_email(email, "register", username=user_name, password=pass_word)  # 发送邮件
            return HttpResponse(json.dumps({"status": "success", "token": token}), content_type="application/json")
        else:
            captcha_error = register_form.errors.setdefault('captcha', "表单验证失败")
            return HttpResponse(json.dumps({"status": "failure", "msg": captcha_error}), content_type="application/json")


class ForgetPwdView(View):
    """忘记密码页面"""
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forget_pwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            user_record = UserProfile.objects.get(email=email)
            if user_record:
                token = send_register_email(email, "forget")  # 发送邮件
                return HttpResponse(json.dumps({"status": "success", "token": token}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "failure", "msg": "该邮箱不存在"}), content_type="application/json")
        else:
            captcha_error = forget_form.errors.setdefault('captcha', "表单验证失败")
            return HttpResponse(json.dumps({"status": "failure", "msg": captcha_error}), content_type="application/json")


class ActiveCodeView(View):
    """激活账号页面"""
    def get(self, request, active_code):
        all_records = EmailVarifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                record.delete()
                request.session.update({"msg": "激活成功", "status": "info"})       # 通过session传递重定向数据
                return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'active_fail.html')
        return render(request, "login.html", {"msg": "链接无效", "status": "danger"})


class SuccessView(View):
    """邮件发送成功页面"""
    def get(self, request, token):
        # 根据凭证查看是否是正确用户
        email_record = EmailVarifyRecord.objects.filter(token=token)
        if email_record:
            return render(request, 'send_success.html')
        else:
            request.session.update({"msg": "本次操作非法", "status": "danger"})  # 通过session传递重定向数据
            return HttpResponseRedirect(reverse('users:login'))


class ResetView(View):
    """重置密码认证链接"""
    def get(self, request, active_code):
        all_records = EmailVarifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "reset_pwd.html", {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, "login.html", {"msg": "链接无效", "status": "danger"})


class ResetPwdView(View):
    """修改密码页面"""
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({"status": "failure", "msg": "密码不一致!", "email": email}), content_type="application/json")
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            try:
                record = EmailVarifyRecord.objects.get(email=email, send_type="forget")
            except:
                return HttpResponse(json.dumps({"status": "failure", "msg": "error", "email": email}), content_type="application/json")
            record.delete()
            return HttpResponse(json.dumps({"status": "success", "email": email}), content_type="application/json")
        else:
            email = request.POST.get("email", '')
            return HttpResponse(json.dumps({"status": "failure", "msg": "表单验证失败!", "email": email}), content_type="application/json")


class RedirectToMyLoginView(View):
    """重定向到自定义登录页面"""
    def get(self, request):
        return HttpResponseRedirect(reverse("users:login"))


def page_not_found(request):
    """全局404页面视图配置"""
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

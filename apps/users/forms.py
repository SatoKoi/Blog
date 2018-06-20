# -*- coding:utf-8 -*-
from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=26, required=True)
    password = forms.CharField(min_length=6, max_length=30, required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(min_length=4, max_length=26, required=True)
    password = forms.CharField(min_length=6, max_length=30, required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(min_length=6, max_length=30, required=True, error_messages={"required": "密码必须大于5位",
                                                                             "invalid": "密码必须大于5位"})
    password2 = forms.CharField(min_length=6, max_length=30, required=True)

    def clean(self):
        """重写clean方法实现自定义表单信息验证及错误信息传递"""
        try:
            _ = self.cleaned_data['password1']
        except Exception:
            raise forms.ValidationError('{}'.format("密码必须大于5位"))

        try:
            _ = self.cleaned_data['password2']
        except Exception:
            raise forms.ValidationError('密码不一致')
        else:
            return self.cleaned_data



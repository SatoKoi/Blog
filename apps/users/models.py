from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """登录用户信息"""
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birth_day = models.DateField(verbose_name="生日", null=True, blank=True)      # 允许为空
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="male")
    image = models.ImageField(verbose_name="用户头像", upload_to="user/%Y/%m", max_length=100, default="default/user.png")

    class Meta:
        verbose_name_plural = verbose_name = "用户信息"

    def __str__(self):
        return self.username


class EmailVarifyRecord(models.Model):
    """邮箱验证记录"""
    code = models.CharField(verbose_name="验证码", max_length=20)
    token = models.CharField(verbose_name="凭证", max_length=26, null=True, blank=True)
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证类型", choices=(("register", "注册"), ("forget", "找回密码")), max_length=15)
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name_plural = verbose_name = "邮箱验证码"

    def __str__(self):
        return "{0}({1})".format(self.code, self.email)

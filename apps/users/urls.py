# -*- coding:utf-8 -*-
from django.urls import path
<<<<<<< HEAD
from .views import LoginView, LogoutView, RegisterView, ForgetPwdView, ActiveCodeView, \
=======
from .views import LoginView, RegisterView, ForgetPwdView, ActiveCodeView, \
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
    SuccessView, ResetView, ResetPwdView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
<<<<<<< HEAD
    path('logout/', LogoutView.as_view(), name='logout'),
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
    path('register/', RegisterView.as_view(), name='register'),
    path('forgetpwd/', ForgetPwdView.as_view(), name='forgetpwd'),
    path('success/<slug:token>/', SuccessView.as_view(), name='success'),
    path('active/<slug:active_code>/', ActiveCodeView.as_view(), name='active'),
    path('reset/<slug:active_code>/', ResetView.as_view(), name='reset'),
    path('resetpwd/', ResetPwdView.as_view(), name='resetpwd'),
]
"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from MyBlog.settings import MEDIA_ROOT
# from MyBlog.settings import STATIC_ROOT
from django.contrib import admin
import xadmin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve
from users.views import RedirectToMyLoginView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'xadmin/login/', RedirectToMyLoginView.as_view(), name="mylogin"),
    path(r'xadmin/', xadmin.site.urls),
    path(r'favicon.ico/', RedirectView.as_view(url=r'/static/favicon.ico', permanent=True)),
    path(r'', include('blog.urls', namespace='blog')),
    path(r'user/', include('users.urls', namespace='users')),
    path(r'captcha/', include('captcha.urls')),
    path(r'ueditor/', include('DjangoUeditor.urls')),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # re_path(r'static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT})  # DEBUG为False时启用
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

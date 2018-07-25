"""
Django settings for MyBlog project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tdzht2p+@%k1ei-$14sm6p)6y=ket^3gbrr^rz-15caefjbmyt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserProfile'       # 重载配置, 更改用户登录表模型

AUTHENTICATION_BACKENDS = (                 # 自定义帐号验证方法
    'users.views.CustomBackend',
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'blog',
    'xadmin',
    'crispy_forms',
    'captcha',
    'DjangoUeditor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'MyBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',
        'HOST': '47.106.72.198',
        'USER': 'root',
        'PASSWORD': '13786836697qwe',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 邮箱设置
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))
from utils.mysql_conc import get_email_account
EMAIL_HOST = 'smtp.sina.com.cn'        # 邮箱客户端
# EMAIL_PORT = 25 		       # 阿里云服务器已关闭25端口
EMAIL_PORT = 587
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = get_email_account('root', '13786836697qwe')
EMAIL_USE_TLS = False
EMAIL_FROM = EMAIL_HOST_USER  # 发件人

# 设置上传文件的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 会话设置
SESSION_SAVE_EVERY_REQUEST = True           # 保存所有请求的会话session
SESSION_COOKIE_AGE = 60 * 30                # cookie有效时间
SESSION_EXPIRE_AT_BROWSER_CLOSE = True      # 关闭浏览器, cookie即失效

DATA_UPLOAD_MAX_MEMORY_SIZE = 31457280      # 最大上传大小30MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240       # 最大数量字段

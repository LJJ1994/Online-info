"""
Django settings for xxz project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5q1w7h@9$e_0(@z3a322d=p5pl!0+ixhz044kol$9sbkzf0-*-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.news',
    'apps.cms',
    'apps.xfzauth',
    'apps.course',
    'apps.payinfo',
    'apps.ueditor',
    'debug_toolbar',
    'haystack',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'xxz.urls'

AUTH_USER_MODEL = 'xfzauth.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'front', 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static'
            ]
        },
    },
]

WSGI_APPLICATION = 'xxz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'Ljj940617',
        'NAME': 'xxz',
        'POST': '3306'
    }
}

# 配置全文搜索
# 指定搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'apps.news.whoosh_cn_backends.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

# 指定如何对搜索结果分页，这里设置为每 10 项结果为一页，默认是 20 项为一页
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# 添加此项，当数据库改变时，会自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# 缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 静态文件配置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front', 'dist')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 七牛云配置
QINIU_ACCESS_KEY = 'DKBwZ3jYFmRUitplgBTkvgvZS5tel4h6HBtZHhHX'
QINIU_SECRET_KEY = 'U0FurqXznNUX7lvF_vpLoN8hxhh7qPOp0-OZnTx_'
QINIU_BUCKET_NAME = 'xfz'
QINIU_DOMAIN = 'http://ptmoolpfo.bkt.clouddn.com/'

# Ueditor配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN

UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR, 'front', 'dist', 'ueditor', 'config.json')

# 加载文章数目
ONE_PAGE_NEWS = 4

# debug-toolbar配置
INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_PANELS = [
    # 代表是哪个django版本
    'debug_toolbar.panels.versions.VersionsPanel',
    # 用来计时的，判断加载当前页面总共花的时间
    'debug_toolbar.panels.timer.TimerPanel',
    # 读取django中的配置信息
    'debug_toolbar.panels.settings.SettingsPanel',
    # 看到当前请求头和响应头信息
    'debug_toolbar.panels.headers.HeadersPanel',
    # 当前请求的想信息（视图函数，Cookie信息，Session信息等）
    'debug_toolbar.panels.request.RequestPanel',
    # 查看SQL语句
    'debug_toolbar.panels.sql.SQLPanel',
    # 静态文件
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 模板文件
    'debug_toolbar.panels.templates.TemplatesPanel',
    # 缓存
    'debug_toolbar.panels.cache.CachePanel',
    # 信号
    'debug_toolbar.panels.signals.SignalsPanel',
    # 日志
    'debug_toolbar.panels.logging.LoggingPanel',
    # 重定向
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': ''
}

# 百度云的配置
# 控制台->用户中心->用户ID
BAIDU_CLOUD_USER_ID = 'ffc4ac9f9be84f31a3d0c60bcb3963a8'
# 点播VOD->全局设置->发布设置->安全设置->UserKey
BAIDU_CLOUD_USER_KEY = '5fe50756068345c6'

# 支付宝配置
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do?"
ALIPAY_APPID = '2016092900625962'

# ALIPAY_NOTIFY_URL = "http://127.0.0.1:8888/pay_result/" # 如果只可以内网访问开发服务器
ALIPAY_NOTIFY_URL = "http://1.203.45.678:8888/pay_result/" # 如果生产环境或外网可以访问开发
ALIPAY_RETURN_URL = "http://1.203.45.678:8888/pay_result/"
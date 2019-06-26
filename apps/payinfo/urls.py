__author__ = 'LJJ'
__date__ = '2019/6/21 上午3:25'

from django.urls import path
from . import views

app_name = 'payinfo'

urlpatterns = [
    path('', views.payinfo, name='payinfo'),
]
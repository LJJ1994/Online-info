__author__ = 'LJJ'
__date__ = '2019/6/21 上午3:25'

from django.urls import path
from . import views

app_name = 'payinfo'

urlpatterns = [
    path('', views.index, name='index'),
    path('payinfo_order/<int:payinfo_id>/', views.payinfo_order, name='payinfo_order'),
    path('payinfo_order_request/', views.payinfo_order_request, name='payinfo_order_request'),
    path('payinfo_order_completed/', views.payinfo_order_completed, name='payinfo_order_completed'),
    path('payinfo_payment_result/', views.payinfo_payment_result, name='payinfo_payment_result'),
]
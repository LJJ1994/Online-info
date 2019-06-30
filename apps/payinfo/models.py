from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.


class PayInfo(models.Model):
    """付费资讯模型"""
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    file = models.FilePathField()


class PayinfoOrder(models.Model):
    """付费资讯订单"""
    uid = ShortUUIDField(primary_key=True)  # 每个订单的uid都不同
    payinfo = models.ForeignKey('PayInfo', on_delete=models.DO_NOTHING, related_name='payinfo_order')
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING, related_name='payinfo_buyer')
    trade_no = models.CharField(max_length=200)
    amount = models.FloatField()
    pub_time = models.DateTimeField(auto_now_add=True)
    is_type = models.SmallIntegerField(default=1)  # 1.代表支付宝支付 2.代表微信支付
    status = models.SmallIntegerField(default=1)  # 1. 代表未支付状态 2.代表已支付状态

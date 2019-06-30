from django.db import models
from shortuuidfield import ShortUUIDField


class CourseCategory(models.Model):
    """课程分类"""
    name = models.CharField(max_length=100)


class Teacher(models.Model):
    """讲师"""
    username = models.CharField(max_length=20)
    avatar = models.URLField()
    profile = models.TextField()
    jobtitle = models.CharField(max_length=100)


class Course(models.Model):
    """课程信息"""
    title = models.CharField(max_length=200)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)


class CourseOrder(models.Model):
    """课程订单"""
    uid = ShortUUIDField(primary_key=True)  # 每个订单的uid都不同
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, related_name='course_order')
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING, related_name='course_order')
    trade_no = models.CharField(max_length=200)
    amount = models.FloatField()
    pub_time = models.DateTimeField(auto_now_add=True)
    is_type = models.SmallIntegerField(default=1)  # 1.代表支付宝支付 2.代表微信支付
    status = models.SmallIntegerField(default=1)  # 1. 代表未支付状态 2.代表已支付状态
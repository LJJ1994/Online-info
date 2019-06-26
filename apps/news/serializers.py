__author__ = 'LJJ'
__date__ = '2019/6/26 上午1:10'

from rest_framework import serializers
from .models import News, NewsCategory
from apps.xfzauth.serializers import UserSerializers


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ('title', 'desc', 'thumbnail', 'author', 'category', 'pub_time')

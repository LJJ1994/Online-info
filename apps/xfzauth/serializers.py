__author__ = 'LJJ'
__date__ = '2019/6/26 上午1:13'

from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'username', 'telephone', 'is_staff', 'is_active', 'email')

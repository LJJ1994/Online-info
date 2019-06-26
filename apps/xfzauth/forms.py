__author__ = 'LJJ'
__date__ = '2019/6/21 上午12:27'

from django import forms
from django.core.cache import cache

from apps.common.forms import FormMixin
from .models import User

class FormLogin(forms.Form, FormMixin):
    """
    登录表单处理
    """
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=50,min_length=6, error_messages=
    {'max_length': '密码最大长度不能超过50个字符', 'min_length': '密码最小长度不能低于6个字符'})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    """
    注册表单处理
    """
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=50,min_length=6, error_messages=
    {'max_length': '密码最大长度不能超过50个字符', 'min_length': '密码最小长度不能低于6个字符'})
    password2 = forms.CharField(max_length=50,min_length=6, error_messages=
    {'max_length': '密码最大长度不能超过50个字符', 'min_length': '密码最小长度不能低于6个字符'})
    img_captcha = forms.CharField(max_length=4, min_length=4, error_messages=
    {'max_length': '验证码大小为4', 'min_length': '验证码大小为4'})
    sms_captcha = forms.CharField(max_length=6, min_length=4, error_messages=
    {'max_length': '验证码为6', 'min_length': '验证码大小为4'})

    def clean(self):
       cleaned_data = super(RegisterForm, self).clean()

       passwrod1 = cleaned_data.get('password1')
       password2 = cleaned_data.get('password2')
       telephone = cleaned_data.get('telephone')
       print('清理过的手机号：',telephone)

       if passwrod1 != password2:
           raise forms.ValidationError('两次密码不一致！')

       img_captcha = cleaned_data.get('img_captcha')
       img_captcha_cache = cache.get(img_captcha.lower())

       if not img_captcha_cache or img_captcha.lower() != img_captcha_cache.lower():
           raise forms.ValidationError('图片验证码不正确！')

       sms_captcha = cleaned_data.get('sms_captcha')
       sms_captcha_cache = cache.get(str(telephone))

       if not sms_captcha_cache or sms_captcha != sms_captcha_cache:
           raise forms.ValidationError('短信验证码不正确!')

       exist = User.objects.filter(telephone=telephone).exists()
       if exist:
           raise forms.ValidationError('该手机号已经被注册!')

       return cleaned_data



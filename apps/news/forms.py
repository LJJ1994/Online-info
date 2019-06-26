__author__ = 'LJJ'
__date__ = '2019/6/27 上午12:18'

from django import forms
from apps.common.forms import FormMixin


class CommentForm(forms.Form, FormMixin):
    news_id = forms.IntegerField()
    content = forms.CharField()
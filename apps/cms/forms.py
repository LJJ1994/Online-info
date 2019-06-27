__author__ = 'LJJ'
__date__ = '2019/6/25 上午4:24'

from django import forms
from apps.common.forms import FormMixin
from apps.news.models import News


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={'required': '必须传入要删除的分类ID！'})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'pub_time', 'author']


class EditNewsForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'pub_time', 'author']

__author__ = 'LJJ'
__date__ = '2019/6/27 下午11:48'

from datetime import datetime
from urllib import parse

from django.shortcuts import render
from django.views.generic import View
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET

from apps.course.models import CourseCategory, Course, Teacher
from .forms import PublicCourseForm, EditNewsCourseCategoryForm, EditCourseForm
from utils import restful


class CourseListView(View):
    def get(self, request):
        """
        通过p获取分页数据
        :param request:?p=xxx
        :return: data
        """
        page = int(request.GET.get('p',1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)

        courses = Course.objects.all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=6,day=1)

            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            courses = courses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            courses = courses.filter(title__icontains=title)

        if category_id:
            courses = courses.filter(category=category_id)

        paginator = Paginator(courses, 2)
        page_obj = paginator.page(page)

        context_data = self.get_paginator_data(paginator, page_obj)

        context = {
            'categories': CourseCategory.objects.all(),
            'courses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }

        print('#'*30)
        print(context['url_query'])
        context.update(context_data)

        return render(request, 'cms/course_list.html', context=context)

    def get_paginator_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count -1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class EditCourseView(View):
    """
    编辑课程类视图
    """
    def get(self, request):
        course_id = request.GET.get('course_id')
        print('course_id------------>%s'%course_id)
        course = Course.objects.get(pk=course_id)
        context = {
            'course': course,
            'teachers': Teacher.objects.all(),
            'categories': CourseCategory.objects.all()
        }

        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        forms = EditCourseForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            category_id = forms.cleaned_data.get('category_id')
            teacher_id = forms.cleaned_data.get('teacher_id')
            video_url = forms.cleaned_data.get('video_url')
            cover_url = forms.cleaned_data.get('cover_url')
            price = forms.cleaned_data.get('price')
            duration = forms.cleaned_data.get('duration')
            profile = forms.cleaned_data.get('profile')

            teacher = Teacher.objects.get(pk=teacher_id)
            category = CourseCategory.objects.get(pk=category_id)

            pk = forms.cleaned_data.get('pk')

            Course.objects.filter(pk=pk).update(title=title, category=category, teacher=teacher, video_url=video_url,
                                  cover_url=cover_url, price=price, duration=duration, profile=profile)

            return restful.ok(message='课程编辑成功!')
        else:
            return restful.param_error(message="表单验证失败!")


class PublicCourseView(View):
    def get(self, request):
        """
        课程发布
        :param request:
        :return:
        """
        context = {
            'teachers': Teacher.objects.all(),
            'categories': CourseCategory.objects.all()
        }

        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        forms = PublicCourseForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            category_id = forms.cleaned_data.get('category_id')
            teacher_id = forms.cleaned_data.get('teacher_id')
            video_url = forms.cleaned_data.get('video_url')
            cover_url = forms.cleaned_data.get('cover_url')
            price = forms.cleaned_data.get('price')
            duration = forms.cleaned_data.get('duration')
            profile = forms.cleaned_data.get('profile')

            teacher = Teacher.objects.get(pk=teacher_id)
            category = CourseCategory.objects.get(pk=category_id)

            Course.objects.create(title=title, category=category, teacher=teacher, video_url=video_url,
                                  cover_url=cover_url, price=price, duration=duration, profile=profile)

            return restful.ok(message='课程发布成功!')


@require_POST
def delete_course(request):
    """
    删除某篇新闻
    :param request: news_id
    :return:
    """
    news_id = request.POST.get('course_id')
    news = Course.objects.filter(pk=news_id)
    news.delete()

    return restful.ok(message='课程删除成功!')


class CourseCategoryView(View):
    def get(self, request):
        categories = CourseCategory.objects.all()
        context = {
            'categories': categories
        }

        return render(request, 'cms/course_category.html', context=context)


@require_POST
def add_course_category(request):
    """
    添加课程分类
    :param request: name
    :return: ok
    """
    name = request.POST.get('name')
    exists = CourseCategory.objects.filter(name=name).exists()

    if not exists:
        CourseCategory.objects.create(name=name)

        return restful.ok(message='创建课程分类成功!')
    else:
        return restful.param_error(message='该课程分类已存在!')


@require_POST
def edit_course_category(request):
    """
    编辑新闻分类
    :param request: pk, name
    :return:
    """
    forms = EditNewsCourseCategoryForm(request.POST)

    if forms.is_valid():
        pk = forms.cleaned_data.get('pk')
        name = forms.cleaned_data.get('name')

        try:
            CourseCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok(message='编辑成功!')
        except:
            return restful.param_error(message='要编辑的分类不存在!')

    else:
        return restful.param_error(message=forms.get_errors())


@require_POST
def delete_course_category(request):
    """
    删除课程分类
    :param request:pk
    :return:
    """
    pk = request.POST.get('pk')
    try:
        CourseCategory.objects.filter(pk=pk).delete()
        return restful.ok(message='删除成功!')
    except:
        return restful.param_error(message='要删除的新闻不存在!')

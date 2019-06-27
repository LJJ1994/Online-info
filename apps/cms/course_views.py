__author__ = 'LJJ'
__date__ = '2019/6/27 下午11:48'
from django.shortcuts import render
from django.views.generic import View

from apps.course.models import CourseCategory, Course, Teacher
from .forms import PublicCourseForm
from utils import restful


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

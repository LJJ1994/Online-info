__author__ = 'LJJ'
__date__ = '2019/7/1 下午12:13'


from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, ContentType, Group

from apps.news.models import News, NewsCategory, Comment
from apps.course.models import Course, CourseCategory, Teacher, CourseOrder
from apps.payinfo.models import PayInfo, PayinfoOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # self.stdout.write(self.style.SUCCESS('hello world!'))
        # 编辑组的权限设置
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(PayInfo),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGroup = Group.objects.create(name='编辑组')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('创建编辑组成功!'))

        # 财务组的权限设置
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayinfoOrder)
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        financeGroup = Group.objects.create(name='财务组')
        financeGroup.permissions.set(finance_permissions)
        financeGroup.save()
        self.stdout.write(self.style.SUCCESS('创建财务组成功!'))

        # 管理员组的权限设置
        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员组')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()

        self.stdout.write(self.style.SUCCESS('创建管理员组成功!'))

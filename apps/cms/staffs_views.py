__author__ = 'LJJ'
__date__ = '2019/7/1 下午1:05'

from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator  # 给类视图添加装饰器的方法
from django.contrib.admin.views.decorators import staff_member_required

from apps.xfzauth.models import User
from apps.xfzauth.decorators import xxz_superuser_required


@staff_member_required(login_url='index')
def staff(request):
    """
    查看员工个人信息
    :param request:
    :return:
    """
    telephone = request.user.telephone
    password = request.user.password
    exist = User.objects.filter(password=password, telephone=telephone).exists()
    if exist:
        username = request.user.username
        email = request.user.email
        telephone = request.user.telephone
        is_staff = request.user.is_staff
        date_joined = request.user.date_joined.strftime('%Y-%m-%d %H:%M:%S')

        context = {
            'username': username,
            'email': email if email else '无',
            'telephone': telephone,
            'is_staff': '是' if is_staff else '否',
            'date_joined': date_joined
        }

        return render(request, 'cms/personal_center.html', context=context)




@xxz_superuser_required
def staffs_views(request):
    """
    员工
    :return: staffs
    """
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs': staffs
    }

    return render(request, 'cms/staff.html', context=context)


@method_decorator(xxz_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }

        return render(request, 'cms/add_staff.html', context=context)

    def post(self, request):
        """
        添加员工权限
        :param request: 1.checkbox里面的value值, 2. telephone
        :return: redirect('cms:staffs')
        """
        # getlist这个方法获取前端checkbox标签里面的name字段的所有id值,返回[id1,id2, id3, id4]
        groupids = request.POST.getlist('groups')
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        print('user-------->:%s'%user)
        user.is_staff = True  # 设置员工属性为True

        groups = Group.objects.filter(pk__in=groupids)
        print('groups---->%s' % groups)
        user.groups.set(groups)  # 将提取到的组设置在当前user用户
        print('user-group----->%s'%user.groups)
        user.save()

        return redirect(reverse('cms:staffs'))

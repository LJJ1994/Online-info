from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not username:
            raise ValueError('请输入用户名！')

        if not telephone:
            raise ValueError('请输入手机号！')

        if not password:
            raise ValueError('请输入密码！')

        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False

        self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    定义用户模型
    """
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=100)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)  # 该用户是否可用
    is_staff = models.BooleanField(default=False)  # 是否为员工
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):

        return self.username

    def get_short_name(self):

        return self.username




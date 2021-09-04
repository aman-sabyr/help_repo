from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, username, password):
        if not username:
            raise ValueError('Username cant be empty')
        user = self.model(username=username)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_user(self, username, password):
        return self._create(username=username, password=password)


class User(AbstractBaseUser):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    email = models.EmailField()
    username = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    education = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        db_table = 'account_user'



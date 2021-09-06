from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, username, password, email):
        if not username:
            raise ValueError('Username cant be empty')
        user = self.model(username=username)
        user.set_password(raw_password=password)
        user.activation_code = get_random_string(length=10)
        email = self.normalize_email(email)
        user.email = email
        user.save()
        print(user.email)
        return user

    def create_user(self, username, password, email):
        return self._create(username=username, password=password, email=email)


class User(AbstractBaseUser):
    email = models.EmailField()
    username = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    education = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    activation_code = models.CharField(blank=True, max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        db_table = 'account_user'



from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts import managers


#Option1 = inherit from AbstractUser
# class CustomUser(AbstractUser):
#     points = models.IntegerField(default=0)

#Option2 = inherit from CustomUser, will not create table, will use User table as its base
# class CustomCustomUser(CustomUser):
#     class Meta:
#         proxy = True
#         def get_points(self):
#             return self.points


#Option3 = inherit from AbstractBaseUser, will give us full control
class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email






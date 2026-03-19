from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserCreationForm

UserModel = get_user_model()
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm

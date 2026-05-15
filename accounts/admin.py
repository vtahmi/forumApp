from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import CustomUserCreationForm
from accounts.models import Profile

UserModel = get_user_model()
@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    model = UserModel
    list_display = ('email', 'username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # махаме 'date_joined'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    @admin.register(Profile)
    class ProfileAdmin(admin.ModelAdmin):
        list_display = ('user', 'age', 'points', 'phone_number')
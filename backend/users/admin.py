from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 定义一个自定义的UserAdmin
class CustomUserAdmin(UserAdmin):
    # 扩展原有的字段集，加入我的自定义字段
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('自定义信息', {'fields': ('role', 'phone_number')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('自定义信息', {'fields': ('role', 'phone_number')}),
    )

    # 在列表页显示自定义字段
    list_display = ["username", "email", "role", "phone_number", "is_staff"]

# 注册我们自定义的User模型和Admin类
admin.site.register(User, CustomUserAdmin)

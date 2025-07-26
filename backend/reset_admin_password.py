from django.contrib.auth import get_user_model

User = get_user_model()
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123456')
    admin.is_staff = True
    admin.is_superuser = True
    admin.is_active = True
    admin.save()
    print("Admin password has been reset successfully.")
except User.DoesNotExist:
    print("Admin user not found.")

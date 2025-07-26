from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates or resets the admin user password'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = 'admin123456'
        email = 'admin@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'User "{username}" already exists. Resetting password and ensuring permissions.')
            user = User.objects.get(username=username)
        else:
            self.stdout.write(f'User "{username}" not found. Creating new user.')
            user = User(username=username, email=email)

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully ensured user "{username}" with password "{password}" exists and has superuser rights.'))

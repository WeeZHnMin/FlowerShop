from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Checks the status of the admin user'

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin.username}" found.'))
            self.stdout.write(f'  - Is staff: {admin.is_staff}')
            self.stdout.write(f'  - Is superuser: {admin.is_superuser}')
            self.stdout.write(f'  - Is active: {admin.is_active}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user "admin" not found in the database.'))

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed an admin user'

    def handle(self, *args, **options):
        email = 'adminlestari@gmail.com'
        password = 'admin123'
        name = 'Admin Lestari'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin user with email {email} already exists.'))
            return

        user = User.objects.create_user(
            username=email,
            email=email,
            name=name,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        Profile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {email}'))

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя
    """
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@sky.pro',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password('123456')
        user.save()

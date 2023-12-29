from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin_one@office_shop.ru',
            first_name='Admin',
            last_name='Adminkin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('Mentos19')
        user.save()

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = "Иван"  # то имя, которое вы пытаетесь создать

        # Проверка на существование
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь с именем "{username}" уже существует!'))
            return

        # Создание, если пользователя нет
        user = User.objects.create_user(username=username, password="12345")
        self.stdout.write(self.style.SUCCESS(f'Пользователь {username} успешно создан!'))
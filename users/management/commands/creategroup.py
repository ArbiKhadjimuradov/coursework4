from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from users.models import CustomUser


class Command(BaseCommand):
    """Команда создания группы пользователей"""
    def handle(self, *args, **options):
        moder_group = Group.objects.create(name='moder_products')  # Создаем группу пользователей
        new_permission = Permission.objects.get(codename='can_view_mailing')  # получаем право доступа
        moder_group.permissions.add(new_permission)  # добавляем право доступа в группу

        user = CustomUser.objects.get(email='mymail.sky@yandex.ru')  # получаем пользователя
        user.groups.add(moder_group)  # добавляем пользователя в группу модераторов

        self.stdout.write(self.style.SUCCESS(f"Successfully created group user this name {moder_group.name}!"))

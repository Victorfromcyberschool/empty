from django.core.management.base import BaseCommand, CommandError

from main.models import Product


class Command(BaseCommand):
    help_text = 'Команда для создания ЧПУ у товаров'

    def handle(self, *args, **kwargs):
        queryset = Product.objects.filter(is_active=True)
        for object in queryset:
            try:
                object.save()
            except CommandError as e:
                print(e)
        print('ЧПУ для товаров успешно созданы')

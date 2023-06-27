# Generated by Django 4.2.2 on 2023-06-27 15:20

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activity',
            field=models.DecimalField(choices=[(Decimal('1'), 'Без учета физ. нагрузки'), (Decimal('1.2'), 'Сидячий образ жизни'), (Decimal('1.375'), 'Легкая активность (1-2 раза в неделю)'), (Decimal('1.55'), 'Умеренная активность (3-5 раз в неделю)'), (Decimal('1.725'), 'Высокая активность (более 5 раз в неделю)'), (Decimal('1.9'), 'Очень высокая активность (профессиональный спорт)')], decimal_places=3, default=1.0, max_digits=5),
        ),
    ]
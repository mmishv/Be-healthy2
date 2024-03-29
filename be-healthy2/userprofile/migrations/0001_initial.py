# Generated by Django 4.2.1 on 2023-06-26 16:17

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/users', verbose_name='Аватар')),
                ('age', models.PositiveSmallIntegerField(null=True)),
                ('height', models.PositiveSmallIntegerField(null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('activity', models.DecimalField(choices=[(Decimal('1'), 'Без учета физ. нагрузки'), (Decimal('1.2'), 'Сидячий образ жизни'), (Decimal('1.375'), 'Легкая активность (1-2 раза в неделю)'), (Decimal('1.55'), 'Умеренная активность (3-5 раз в неделю)'), (Decimal('1.725'), 'Высокая активность (более 5 раз в неделю)'), (Decimal('1.9'), 'Очень высокая активность (профессиональный спорт)')], decimal_places=3, default=1.0, max_digits=4)),
                ('goal', models.DecimalField(choices=[(Decimal('1'), 'Поддержание веса'), (Decimal('1.2'), 'Набор веса'), (Decimal('0.8'), 'Снижение веса')], decimal_places=1, default=1, max_digits=2)),
                ('sex', models.CharField(choices=[('F', 'Женский'), ('M', 'Мужской')], default='F', max_length=1)),
                ('role', models.CharField(choices=[('U', 'Обычный пользователь'), ('A', 'Администратор')], default='U', max_length=1)),
                ('calories', models.DecimalField(decimal_places=1, default=2000.0, max_digits=5)),
                ('proteins', models.DecimalField(decimal_places=1, default=90.0, max_digits=4)),
                ('fats', models.DecimalField(decimal_places=1, default=60.0, max_digits=4)),
                ('carbohydrates', models.DecimalField(decimal_places=1, default=250.0, max_digits=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]

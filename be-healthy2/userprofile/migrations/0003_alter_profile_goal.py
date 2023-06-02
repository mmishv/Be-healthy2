# Generated by Django 4.2.1 on 2023-06-02 15:19

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_alter_profile_activity_alter_profile_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='goal',
            field=models.DecimalField(choices=[(Decimal('1'), 'Поддержание веса'), (Decimal('1.2'), 'Набор веса'), (Decimal('0.8'), 'Снижение веса')], decimal_places=1, default=1, max_digits=2),
        ),
    ]
from _decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class SexOptions(models.TextChoices):
    FEMALE = 'F', 'Женский'
    MALE = 'M', 'Мужской'


ACTIVITY_CHOICES = [
    (Decimal('1'), 'Без учета физ. нагрузки'),
    (Decimal('1.2'), 'Сидячий образ жизни'),
    (Decimal('1.375'), 'Легкая активность (1-2 раза в неделю)'),
    (Decimal('1.55'), 'Умеренная активность (3-5 раз в неделю)'),
    (Decimal('1.725'), 'Высокая активность (более 5 раз в неделю)'),
    (Decimal('1.9'), 'Очень высокая активность (профессиональный спорт)'),
]

GOAL_CHOICES = [
    (Decimal('1'), 'Поддержание веса'),
    (Decimal('1.2'), 'Набор веса'),
    (Decimal('0.8'), 'Снижение веса'),
]


class RoleOptions(models.TextChoices):
    USER = 'U', 'Обычный пользователь'
    ADMIN = 'A', 'Администратор'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    avatar = models.ImageField(upload_to='images/users', verbose_name='Аватар', null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True)
    height = models.PositiveSmallIntegerField(null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    activity = models.DecimalField(choices=ACTIVITY_CHOICES, default=1.0, max_digits=5, decimal_places=3)
    goal = models.DecimalField(choices=GOAL_CHOICES, default=1, max_digits=2, decimal_places=1)
    sex = models.CharField(max_length=1, choices=SexOptions.choices, default=SexOptions.FEMALE)
    role = models.CharField(max_length=1, choices=RoleOptions.choices, default=RoleOptions.USER)
    calories = models.DecimalField(max_digits=5, decimal_places=1, default=2000.0)
    proteins = models.DecimalField(max_digits=4, decimal_places=1, default=90.0)
    fats = models.DecimalField(max_digits=4, decimal_places=1, default=60.0)
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=1, default=250.0)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @property
    def calories_recommendation(self):
        if not self.weight or not self.height or not self.age:
            return 0
        return int(447.6 + 9.2 * float(
            self.weight) + 3.1 * self.height - 4.3 * self.age if self.sex == 'F' else 88.36 + 13.4 * float(
            self.weight) + 4.8 * self.height - 5.7 * self.age * float(self.activity) * float(self.goal))

    @property
    def proteins_recommendation(self):
        return int(self.calories_recommendation * 0.3/4)

    @property
    def fats_recommendation(self):
        return int(self.calories_recommendation * 0.3/9)

    @property
    def carbohydrates_recommendation(self):
        return int(self.calories_recommendation * 0.4/4)

from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class SexOptions(models.TextChoices):
    FEMALE = 'F', 'Женский'
    MALE = 'M', 'Мужской'


# class ActivityChoices(models.Choices):
#     BASE = 1, 'Без учета физ. нагрузки'
#     PASSIVE = 1.2, 'Сидячий образ жизни'
#     LIGHT = 1.375, 'Легкая активность (1-2 раза в неделю)'
#     MODERATE = 1.55, 'Умеренная активность (3-5 раз в неделю)'
#     HIGH = 1.725, 'Высокая активность (более 5 раз в неделю)'
#     SUPER = 1.9, 'Очень высокая активность (профессиональный спорт)'
#
#
# class GoalChoices(models.Choices):
#     MAINTENANCE = (1, 'Поддержание веса')
#     GAIN = (1.2, 'Набор веса')
#     LOSS = (0.8, 'Снижение веса')

ACTIVITY_CHOICES = [
    (1, 'Без учета физ. нагрузки'),
    (1.2, 'Сидячий образ жизни'),
    (1.375, 'Легкая активность (1-2 раза в неделю)'),
    (1.55, 'Умеренная активность (3-5 раз в неделю)'),
    (1.725, 'Высокая активность (более 5 раз в неделю)'),
    (1.9, 'Очень высокая активность (профессиональный спорт)'),
]

GOAL_CHOICES = [
    (1, 'Поддержание веса'),
    (1.2, 'Набор веса'),
    (0.8, 'Снижение веса'),
]


class RoleOptions(models.TextChoices):
    USER = 'U', 'Обычный пользователь'
    ADMIN = 'A', 'Администратор'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    avatar = models.ImageField(upload_to='images/users', verbose_name='Аватар')
    age = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.DecimalField(choices=ACTIVITY_CHOICES, default=1.0, max_digits=4, decimal_places=3)
    goal = models.DecimalField(choices=GOAL_CHOICES, default=1, max_digits=2, decimal_places=1)
    sex = models.CharField(max_length=1, choices=SexOptions.choices, default=SexOptions.FEMALE)
    role = models.CharField(max_length=1, choices= RoleOptions.choices, default=RoleOptions.USER)
    calories = models.DecimalField(max_digits=4, decimal_places=1, default=2000.0)
    proteins = models.DecimalField(max_digits=4, decimal_places=1, default=90.0)
    fats = models.DecimalField(max_digits=4, decimal_places=1, default=60.0)
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=1, default=250.0)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
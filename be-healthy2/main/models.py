from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    title = models.CharField('Название', max_length=200)
    full_text = models.TextField('Текст статьи')
    date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор статьи'
    )
    moderated = models.BooleanField('')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/article{self.id}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


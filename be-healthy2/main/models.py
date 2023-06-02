from django.db import models
from django.urls import reverse

from userprofile.models import Profile
from autoslug import AutoSlugField


class ArticleCategory(models.Model):
    name = models.CharField('Категория', max_length=150, unique=True)
    slug = AutoSlugField(populate_from='name', allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статьи'


class Article(models.Model):
    title = models.CharField('Название', max_length=200)
    full_text = models.TextField('Текст статьи')
    date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор статьи'
    )
    categories = models.ManyToManyField(ArticleCategory, verbose_name='Категории', related_name='articles')
    slug = AutoSlugField(populate_from='title', allow_unicode=True)
    moderated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'id': self.id, 'slug': self.slug})

    class Meta:
        ordering = ('-date', '-title')
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'




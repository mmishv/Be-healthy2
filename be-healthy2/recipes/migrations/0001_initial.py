import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(choices=[('гр.', 'гр.'), ('мл.', 'мл.'), ('шт.', 'шт.'), ('ст.', 'ст.'), ('ст. л.', 'ст. л.'), ('ч. л.', 'ч. л.')], default='гр.', verbose_name='Единица измерения')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'ordering': ('quantity', 'product'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Продукт')),
                ('calories', models.DecimalField(decimal_places=1, max_digits=5)),
                ('proteins', models.DecimalField(decimal_places=1, max_digits=4)),
                ('fats', models.DecimalField(decimal_places=1, max_digits=4)),
                ('carbohydrates', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Категория')),
                ('slug', autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from='name')),
            ],
            options={
                'verbose_name': 'Категория рецепта',
                'verbose_name_plural': 'Категории рецепта',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовления в минутах')),
                ('text', models.TextField(verbose_name='Рецепт')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('slug', autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from='title')),
                ('moderated', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('categories', models.ManyToManyField(related_name='recipes', to='recipes.recipecategory', verbose_name='Категории')),
                ('ingredients', models.ManyToManyField(to='recipes.product', through='Ingredient', related_name='recipes')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.product'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
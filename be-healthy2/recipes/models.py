from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

UNIT_CHOICES = [
    ("гр.", "гр."),
    ("мл.", "мл."),
    ("шт.", "шт."),
    ("ст.", "ст."),
    ("ст. л.", "ст. л."),
    ("ч. л.", "ч. л."),
]


class RecipeCategory(models.Model):
    name = models.CharField('Категория', max_length=150, unique=True)
    slug = AutoSlugField(populate_from='name', allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория рецепта'
        verbose_name_plural = 'Категории рецепта'


class Product(models.Model):
    name = models.CharField('Продукт', max_length=150, unique=True)
    calories = models.DecimalField(max_digits=5, decimal_places=1)
    proteins = models.DecimalField(max_digits=4, decimal_places=1)
    fats = models.DecimalField(max_digits=4, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    title = models.CharField('Название', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор рецепта')
    image = models.ImageField('Изображение', upload_to='images/recipes')
    cooking_time = models.IntegerField('Время приготовления в минутах')
    ingredients = models.ManyToManyField(Product, through='Ingredient', related_name='recipes')
    categories = models.ManyToManyField(RecipeCategory, verbose_name='Категории', related_name='recipes')
    text = models.TextField('Рецепт')
    date = models.DateTimeField('Дата', auto_now_add=True)
    slug = AutoSlugField(populate_from='title', allow_unicode=True)
    moderated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.author}, {self.date}'

    def get_absolute_url(self):
        return f'/{self.id}/{self.slug}'

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    @property
    def kbju_per_100_grams(self):
        kbju = {'k': 0, 'b': 0, 'j': 0, 'u': 0}
        quantity = 0
        for ingredient in self.ingredients.through.objects.filter(recipe=self):
            quantity += ingredient.quantity
            kbju['k'] = kbju['k'] + ingredient.quantity * float(ingredient.product.calories)
            kbju['b'] = kbju['b'] + ingredient.quantity * float(ingredient.product.proteins)
            kbju['j'] = kbju['j'] + ingredient.quantity * float(ingredient.product.fats)
            kbju['u'] = kbju['u'] + ingredient.quantity * float(ingredient.product.carbohydrates)
        if quantity:
            for k, v in kbju.items():
                kbju[k] = round(v / quantity, 1)
        return kbju


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_amount')
    unit = models.CharField('Единица измерения', choices=UNIT_CHOICES, default='гр.')
    quantity = models.IntegerField('Количество', validators=[MinValueValidator(1)])

    class Meta:
        ordering = ('quantity', 'product',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'recipe'),
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.product.name}, {self.quantity} {self.unit}'





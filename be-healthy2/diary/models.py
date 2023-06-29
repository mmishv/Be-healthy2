from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from recipes.models import Product, UNIT_CHOICES


class Meal(models.Model):
    name = models.CharField('Название', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    products = models.ManyToManyField(Product, through='MealProduct', related_name='meals')
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return f'Meal: {self.user}, {self.date}'

    class Meta:
        ordering = ('date', 'name')
        verbose_name = 'прием пищи'
        verbose_name_plural = 'приемы пищи'

    @property
    def kbju_with_quantity(self):
        kbju = {'k': 0, 'b': 0, 'j': 0, 'u': 0, 'quantity': 0}
        for product in self.products.through.objects.filter(recipe=self):
            kbju['k'] = kbju['k'] + product.quantity * float(product.product.calories)
            kbju['b'] = kbju['b'] + product.quantity * float(product.product.proteins)
            kbju['j'] = kbju['j'] + product.quantity * float(product.product.fats)
            kbju['u'] = kbju['u'] + product.quantity * float(product.product.carbohydrates)
            kbju['quantity'] = kbju['quantity'] + product.quantity
        return kbju


class MealProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='product_amount')
    unit = models.CharField('Единица измерения', choices=UNIT_CHOICES, default='гр.')
    quantity = models.IntegerField('Количество', validators=[MinValueValidator(1)])

    class Meta:
        ordering = ('quantity', 'product',)
        verbose_name = 'продукт приема пищи'
        verbose_name_plural = 'продукты приема пищи'
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'meal'),
                name='unique_meal_product'
            )
        ]

    def __str__(self):
        return f'{self.product.name}, {self.quantity} {self.unit}'

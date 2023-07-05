from rest_framework import serializers

from recipes.models import RecipeCategory, Ingredient, Recipe, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'calories', 'proteins', 'fats', 'carbohydrates']


class IngredientSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ['id', 'product', 'unit', 'quantity']


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('id', 'name')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, write_only=True)
    categories = RecipeCategorySerializer(many=True)
    kbju_per_100_grams = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_kbju_per_100_grams(self, obj):
        kbju = obj.kbju_per_100_grams
        return {'k': kbju['k'], 'b': kbju['b'], 'j': kbju['j'], 'u': kbju['u']}

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientSerializer(instance.ingredient_amount.all(), many=True).data
        return representation



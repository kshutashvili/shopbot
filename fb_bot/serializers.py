from rest_framework import serializers
from bot.models import Category
from catalog.models import ProductCategory, Product


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('name', 'slug')


class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = ('name', 'slug', 'description')


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('name', 'photo', 'size', 'price')
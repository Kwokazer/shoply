from rest_framework import serializers
from shop.models import *







class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    structure = ComponentSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'count', 'photo', 'category', 'structure')


class CharacterSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Character
        fields = ('id', 'name', 'description', 'products', 'photo', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'products', 'total', 'status', 'user', 'created_at')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    def validate(self, data):
        count = data.get('count')
        if count is None:
            raise serializers.ValidationError('Поле count - обязательное поле')

        if int(count) <= 0:
            raise serializers.ValidationError('Поле count - положительное число')

        return data

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'count')


class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'photo', 'link', 'author', 'created_at', 'archive_at')


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CharacterUserRelationship
        fields = ('id', 'user', 'created_at', 'rate')

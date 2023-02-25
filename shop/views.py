from datetime import datetime
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import *


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def cart(self, request, pk):
        cart = Cart.objects.filter(user_id=pk)
        data = {
            'user': UserSerializer(User.objects.get(pk=pk)).data,
            'cart': list(map(lambda x: {'product': ProductSerializer(x.product).data, 'count': x.count}, cart))
        }

        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['count', 'price']

    @action(methods=['get'], detail=False)
    def all(self, request):
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)

        return Response(product_serializer.data)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']

    @action(methods=['get'], detail=False)
    def all(self, request):
        characters = Character.objects.all()
        character_serializer = CharacterSerializer(characters, many=True)

        return Response(character_serializer.data)

    @action(methods=['get', 'post'], detail=True)
    def rating(self, request, pk):
        if request.method == 'GET':
            rating = CharacterUserRelationship.objects.filter(character_id=pk)
            data = RatingSerializer(rating, many=True).data

            return Response(data)

        if request.user:
            rate = int(request.POST['rating'])
            author = request.user

            if not rate:
                raise serializers.ValidationError('Поле rate является обязательным для заполнения.')

            character_rating = CharacterUserRelationship.objects.create(rate=rate, user_id=author.pk, character_id=pk)
            character_rating_serializer = RatingSerializer(character_rating)

            return Response(character_rating_serializer.data)

        raise serializers.ErrorDetail('Учетные данные не были предоставлены')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['status', 'user']
    ordering_fields = ['created_at', 'total']

    @action(methods=['get'], detail=False)
    def all(self, request):
        orders = Order.objects.all()
        order_serializer = OrderSerializer(orders, many=True)

        return Response(order_serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['count']
    permission_classes = [IsAdminUser]


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.filter(Q(started_at__lte=datetime.now()) & Q(archive_at__gt=datetime.now()))
    serializer_class = AdvertisementSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'archive_at']

    @action(methods=['get'], detail=False)
    def all(self, request):
        ads = Advertisement.objects.all()
        ads_serializer = AdvertisementSerializer(ads, many=True)

        return Response(ads_serializer.data)

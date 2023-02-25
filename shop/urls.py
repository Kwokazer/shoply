from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'characters', CharacterViewSet, basename='characters')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'ads', AdvertisementViewSet, 'ads')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = router.urls

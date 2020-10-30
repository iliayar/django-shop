from django.urls import path, re_path, include
from rest_framework import routers

from .views import ProductViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions

from shop.models import Product, Category

from .serializers import ProductSerializer, CategorySerializer
from django_shop.authentication import SingleAdminAuthentication

class DefaultMixin(object):
    authentication_classes = (
        # authentication.BasicAuthentication,
        SingleAdminAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

class ProductViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

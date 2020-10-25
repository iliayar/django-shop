from django.urls import path, reverse, re_path

from . import views

urlpatterns = [
    path('', views.index),
    path('warranty', views.static_page('warranty')),
    path('about', views.static_page('about')),
    path('payment', views.static_page('payment')),
    path('delivery', views.static_page('delivery')),
    re_path('^category/(?P<id>\d+)', views.category, name='category'),
    re_path('^product/(?P<id>\d+)', views.product, name='product')
]

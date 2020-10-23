from django.urls import path

from .views import static_page

urlpatterns = [
    path('', static_page('index')),
    path('warranty', static_page('warranty')),
    path('about', static_page('about')),
    path('payment', static_page('payment')),
    path('delivery', static_page('delivery')),
]

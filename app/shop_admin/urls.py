from django.urls import path, re_path

from .views import shop_admin, admin_product, admin_edit, admin_edit_category, admin_category, admin_delete_category

urlpatterns = [
    path('', shop_admin, name='admin_index'),

    re_path('^(?P<id>\d+|new)', admin_product, name='admin_product'),
    path('edit', admin_edit, name='admin_edit'),

    path('edit_category', admin_edit_category, name='admin_edit_category'),
    path('delete_category', admin_delete_category, name='admin_delete_category'),
    re_path('^category/(?P<id>\d+|new)', admin_category, name='admin_category')
]

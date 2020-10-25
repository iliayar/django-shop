from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.shop_admin, name='admin_index'),

    re_path('^(?P<id>\d+|new)', views.admin_product, name='admin_product'),
    path('edit', views.admin_edit, name='admin_edit'),
    path('delete', views.admin_delete, name='admin_delete'),
    path('image', views.admin_image, name='admin_image'),

    path('edit_category', views.admin_edit_category, name='admin_edit_category'),
    path('delete_category', views.admin_delete_category, name='admin_delete_category'),
    re_path('^category/(?P<id>\d+|new)', views.admin_category, name='admin_category')
]

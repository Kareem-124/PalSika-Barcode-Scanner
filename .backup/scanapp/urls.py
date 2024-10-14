from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/<str:code>/', views.scan_barcode, name='scan_barcode'),
    path('add-product/<str:product_id>/', views.add_product_page, name='add_product_page'),
    path('add-product_page/', views.add_product_page, name='add_product_page'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit_product_page/<str:product_id>/', views.edit_product_page, name='edit_product_page'),
    path('edit_product_process/', views.edit_product_process, name='edit_product_process'),
    path('search_for_product_page/', views.search_for_product_page, name='search_for_product_page'),

]

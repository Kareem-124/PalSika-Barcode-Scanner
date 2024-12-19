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
    path('orders_dashboard_page/', views.orders_dashboard_page, name='orders_dashboard_page'),
    path('create_new_order_page/', views.create_new_order_page, name='create_new_order_page'),
    path('create_new_order_process/', views.create_new_order_process, name='create_new_order_process'),
    path('orders_page/', views.orders_page, name='orders_page'),
    path('order_page_products_request/<str:orderID>/', views.order_page_products_request, name='order_page_products_request'),
    path('order_page_assign_new_driver/', views.order_page_assign_new_driver, name='order_page_assign_new_driver'),
    path('create_new_driver_page/', views.create_new_driver_page, name='create_new_driver_page'),
    path('add_driver_process/', views.add_driver_process, name='add_driver_process'),
    path('edit_driver_page/<int:driver_id>/', views.edit_driver_page, name='edit_driver_page'),
    path('edit_driver_process/<int:driver_id>/', views.edit_driver_process, name='edit_driver_process'),
    path('edit_customer_page/<int:customerID>/', views.edit_customer_page, name='edit_customer_page'),
    path('edit_customer_process/<int:customerID>/', views.edit_customer_process, name='edit_customer_process'),
    path('edit_order_card_page/<int:order_card_id>/', views.edit_order_card_page, name='edit_order_card_page'),
    path('edit_order_card_process/<int:order_card_id>/', views.edit_order_card_process, name='edit_order_card_process'),
    path('create_new_order_card_page/', views.create_new_order_card_page, name='create_new_order_card_page'),
    path('create_new_order_card_process/', views.create_new_order_card_process, name='create_new_order_card_process'),
    path('show_orders_page/', views.show_orders_page, name='show_orders_page'),
    path('sop_page/', views.sop_page, name='sop_page'),
    path('sop_page_request_product_data/', views.sop_page_request_product_data, name='sop_page_request_product_data'),
    path('sop_sell_request/', views.sop_sell_request, name='sop_sell_request'),
    path('sop_buy_page/', views.sop_buy_page, name='sop_buy_page'),
    path('sop_buy_request/', views.sop_buy_request, name='sop_buy_request'),


]

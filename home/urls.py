from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('buscar_dados/<str:app_modelo>/',views.buscar_dados, name='buscar_dados'),
    
    ############################## PRODUTO ####################################
    path('produto/', views.produto, name='produto'),
    path('form_produto/', views.form_produto, name='form_produto'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('remover_produto/<int:id>/', views.remover_produto, name='remover_produto'),
    path('ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),
    
    ############################## CLIENTE ####################################
    path('cliente/', views.cliente, name='cliente'),
    path('form_cliente/', views.form_cliente, name='form_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('remover_cliente/<int:id>/', views.remover_cliente, name='remover_cliente'),

    ############################### PEDIDO #####################################
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/<int:pedido_id>/', views.detalhar_pedido, name='detalhar_pedido'),
    path('novo_pedido/<int:id_cliente>/',views.novo_pedido, name='novo_pedido'),
    path('pedido/item/<int:item_id>/editar/', views.editar_item_pedido, name='editar_item_pedido'),
    path('pedido/item/<int:item_id>/remover/', views.remover_item_pedido, name='remover_item_pedido'),
    path('remover_pedido/<int:id>/', views.remover_pedido, name='remover_pedido'),
    path('form_pagamento/<int:id>/', views.form_pagamento, name='form_pagamento'),    
    path('editar_pagamento/<int:id>/', views.editar_pagamento, name='editar_pagamento'),
    path('remover_pagamento/<int:id>/', views.remover_pagamento, name='remover_pagamento'),   
]
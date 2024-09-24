from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('user/', views.user, name="user"),
    ############################## CLIENTE ####################################
    path('produto/', views.produto, name='produto'),
    path('form_produto/', views.form_produto, name='form_produto'),
    path('buscar-categorias/', views.buscar_categorias, name='buscar_categorias'),
    path('buscar_dados/<str:app_modelo>/',views.buscar_dados, name='buscar_dados'),
    ############################## CLIENTE ####################################
    path('cliente/', views.cliente, name='cliente'),
    path('form_cliente/', views.form_cliente, name='form_cliente'),
    ############################### PEDIDO #####################################
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/<int:pedido_id>/', views.detalhar_pedido, name='detalhar_pedido'),
    path('novo_pedido/<int:id_cliente>/',views.novo_pedido, name='novo_pedido'),
]
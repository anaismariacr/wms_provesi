from django.urls import path
from . import views

urlpatterns = [
    path("pendientes/", views.pedidos_pendientes, name="pedidos_pendientes"),
    path("todos/", views.pedidos_todos, name="todos_pedidos"),
    path("lista/", views.pedidos_lista, name="pedidos_lista"),
    path('<str:pedido_id>/actualizar-estado/', 
         views.actualizar_estado_pedido, 
         name='actualizar_estado_pedido'),
]

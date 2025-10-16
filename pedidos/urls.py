from django.urls import path
from . import views

urlpatterns = [
    path("pendientes/", views.pedidos_pendientes, name="pedidos_pendientes"),
    path("todos/", views.pedidos_todos, name="todos_pedidos"),
]
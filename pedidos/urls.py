

from django.contrib import admin
from django.urls import path, include
from . import views  # importa la vista que acabas de crear

urlpatterns = [
    path("pendientes/", views.pedidos_pendientes, name="pedidos_pendientes"),
    path("todos/", views.pedidos_todos, name="todos_pedidos"),
    path("", views.pedidos_lista, name="pedidos_lista"),
    path("home/", views.home, name="home"),
]

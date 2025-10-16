from django.shortcuts import render
from django.http import JsonResponse
from .models import Pedido

def pedidos_pendientes(request):
    """
    Vista para consultar los pedidos con estado 'PENDIENTE'.
    Retorna la información en formato JSON, optimizada para pruebas de rendimiento (ASR-1).
    """
    pedidos = (
        Pedido.objects
        .filter(estado="PENDIENTE")
        .values("id", "cliente", "total", "estado", "fecha_creacion")
        .order_by("-fecha_creacion")
    )
    data = list(pedidos)
    return JsonResponse(data, safe=False)

def pedidos_todos(request):
    """
    Vista para consultar los pedidos con estado 'PENDIENTE'.
    Retorna la información en formato JSON, optimizada para pruebas de rendimiento (ASR-1).
    """
    pedidos = (
        Pedido.objects
        .values("id", "cliente", "total", "estado", "fecha_creacion")
        .order_by("-fecha_creacion")
    )
    data = list(pedidos)
    return JsonResponse(data, safe=False)
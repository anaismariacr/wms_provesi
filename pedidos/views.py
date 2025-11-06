from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Pedido
from django.utils import timezone

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

def pedidos_lista(request):
    """
    Vista amigable que muestra todos los pedidos en una tabla HTML.
    """
    
    if request.method == "POST":
        id_pedido = request.POST.get("id")
        cliente = request.POST.get("cliente")
        total = request.POST.get("total")
        estado = request.POST.get("estado")
        
        if id_pedido and cliente and total:
            Pedido.objects.create(
                id=id_pedido,
                cliente=cliente,
                total=total,
                estado=estado or "PENDIENTE",
                fecha_creacion=timezone.now(),
            )
            
        return redirect("pedidos_lista")
    
    estado_filtro = request.GET.get("estado")
    search_query = request.GET.get("search")
        
    pedidos = Pedido.objects.all().order_by("-fecha_creacion")
    
    if estado_filtro and estado_filtro != "TODOS":
        pedidos = pedidos.filter(estado = estado_filtro)
        
    if search_query:
        pedidos = pedidos.filter(cliente__icontains=search_query) | pedidos.filter(id__icontains=search_query)
        
    estados = ["TODOS"] + [e[0] for e in Pedido.ESTADOS]
        
    
    
    return render(request, 
                  "pedidos/lista_pedidos.html", 
                  {"pedidos": pedidos, "estados": estados, "estado_filtro": estado_filtro or "TODOS", "search_query": search_query or ""})
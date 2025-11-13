from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Pedido
from django.utils import timezone
from wms_provesi.auth0backend import getRole

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
    role = getRole(request)
    if role != "Operario Bodega":
        return render(request, "sin_permiso.html")
    
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        nuevo_estado = request.POST.get("estado")
        
        if pedido_id and nuevo_estado:
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            pedido.estado = nuevo_estado
            
            if nuevo_estado == "ENTREGADO":
                pedido.fecha_entrega = timezone.now().date()
                
            else:
                pedido.fecha_entrega = None
                
            pedido.save()
            
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
    
def home(request):
    "Vista para hacer login y acceder a pagina de pedidos"
    return render(request, 'home.html')
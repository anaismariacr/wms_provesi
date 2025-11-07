from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Pedido
from django.utils import timezone
from django.views.decorators.http import require_POST

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
    
@require_POST
def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    nuevo_estado = request.POST.get('estado')

    # Si tienes choices definidos en el modelo, mejor validar contra ellos:
    # if nuevo_estado in dict(Pedido.ESTADOS).keys():
    if nuevo_estado:
        pedido.estado = nuevo_estado
        pedido.save()

    # Vuelves a la lista de pedidos
    return redirect('pedidos_lista')
def pedidos_lista(request):
    """
    Vista amigable que muestra todos los pedidos en una tabla HTML.
    """
    
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

from django.contrib import admin
from .models import Pedido

# Register your models here.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'total', 'fecha_creacion', 'fecha_entrega')
    list_filter = ('estado',)
    search_fields = ('id', 'cliente')
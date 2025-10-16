from django.db import models

# Create your models here.
class Pedido(models.Model):
    ESTADOS = [
        ('TRANSITO', 'transito'),
        ('ALISTAMIENTO', 'alistamiento'),
        ('POR_VERIFICAR', 'por_verificar'),
        ('VERIFICADO', 'verificado'),
        ('EMPACADO_POR_DESPACHAR', 'empacado_por_despachar'),
        ('DESPACHADO', 'despachado'),
        ('DESPACHADO_POR_FACTURAR', 'despachado_por_facturar'),
        ('ENTREGADO', 'entregado'),
        ('DEVUELTO', 'devuelto'),
        ('PRODUCCION', 'produccion'),
        ('BORDADO', 'bordado'),
        ('DROPSHIPPING', 'dropshipping'),
        ('COMPRA', 'compra'),
        ('ANULADO', 'anulado'),
    ]
    
    id = models.CharField(max_length=20, unique=True, primary_key=True)
    cliente = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrega = models.DateField(null=True, blank=True)
    fotos_abierto = models.CharField(max_length=255, null=True, blank=True)
    fotos_cerrado = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.estado}"
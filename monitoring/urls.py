from django.contrib import admin
from django.urls import include, path
from . import views
from pedidos import views as pedidos_views  # 👈 importa las vistas de pedidos

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 NUEVO: la raíz usa pedidos_lista, que sí trae los datos
    path('', pedidos_views.pedidos_lista, name='home'),

    # el resto de rutas del proyecto
    path('', include('measurements.urls')),
    path('', include('variables.urls')),
    path('health-check/', views.healthCheck),
    path('pedidos/', include('pedidos.urls')),
]

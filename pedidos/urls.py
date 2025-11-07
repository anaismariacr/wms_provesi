

from django.contrib import admin
from django.urls import path, include
from . import views  # importa la vista que acabas de crear

urlpatterns = [
    path('admin/', admin.site.urls),

    # apps secundarias (siguen funcionando si las necesitas)
    path('measurements/', include('measurements.urls')),
    path('variables/', include('variables.urls')),
    path('pedidos/', include('pedidos.urls')),

    # NUEVO: front principal → renderiza lista_pedidos.html
    path('', views.home, name='home'),
]

```markdown
# Notas para habilitar caching en la MonitoringApp (Django)

Para comparar cache frío vs cache caliente conviene que el endpoint /measurements o /orders/pending (según tu app) tenga algún tipo de cache. Opciones:

1) Cache en memoria (locmem) - fácil para pruebas en una sola instancia.
2) Redis - recomendado si tienes múltiples instancias (compartido entre instancias).

Ejemplo (settings.py):

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

Para Redis (recomendado con múltiples instancias):
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://<REDIS_HOST>:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
    }
}

Ejemplo de uso en vista (decorator):
from django.views.decorators.cache import cache_page

@cache_page(60)  # cache por 60 segundos
def measurements_view(request):
    ...

Indicaciones para pruebas:
- Cold cache: reinicia app o limpia cache: `python manage.py cache_clear` (si implementas management command) o reinicia instancia.
- Hot cache: pre-warm: curl/requests durante 1-2 min antes de la prueba.

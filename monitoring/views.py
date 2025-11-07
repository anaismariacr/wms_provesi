from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'lista_pedidos.html')

def healthCheck(request):
    return HttpResponse('ok')

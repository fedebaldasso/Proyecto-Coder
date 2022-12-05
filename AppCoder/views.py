from django.shortcuts import render
from .models import Curso
from django.http import HttpResponse

# Create your views here.

def curso(request):
    cursito=Curso(nombre="Python", comision=34645)
    cursito.save()
    cadena_texto=f"curso guardado: Nombre {cursito.nombre}, Comision: {cursito.comision}"
    return HttpResponse(cadena_texto)

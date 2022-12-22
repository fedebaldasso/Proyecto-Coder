from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Persona
from django.http import HttpResponse
from django.urls import reverse_lazy
from AppCoder.forms import CursoForm, ProfeForm, PersonaForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

def curso(request):
    cursito=Curso(nombre="Python", comision=34645)
    cursito.save()
    cadena_texto=f"curso guardado: Nombre {cursito.nombre}, Comision: {cursito.comision}"
    return HttpResponse(cadena_texto)

def cursos(request):
    return render (request, "AppCoder/cursos.html")

def estudiantes(request):
    return render (request, "AppCoder/estudiantes.html")

def profesores(request):
    return render (request, "AppCoder/profesores.html")

def entregables(request):
    return render (request, "AppCoder/entregables.html")

def inicio(request):
    return render (request, "AppCoder/inicio.html")

"""def cursoFormulario(request):
    if request.method=="POST":
        nombre=request.POST["nombre"]
        comision=request.POST["comision"]
        print(nombre,comision)
        curso= Curso(nombre=nombre, comision=comision)
        curso.save()
        return render (request, "AppCoder/inicio.html", {"mensaje": "Curso guardado correctamente"})

    else:
        return render (request, "AppCoder/cursoFormulario.html")"""

def cursoFormulario(request):  # Creación de formulario
    if request.method=="POST":
        form= CursoForm(request.POST) #por POST el formulario viene lleno
        print("----------------")
        print(form)
        print("----------------")
        if form.is_valid():
            informacion=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            print(informacion)
            nombre=informacion["nombre"]
            comision=informacion["comision"]            
            curso= Curso(nombre=nombre, comision=comision)
            curso.save()
            return render (request, "AppCoder/inicio.html", {"mensaje": "Curso guardado correctamente"})
        else:
            return render (request, "AppCoder/cursoFormulario.html", {"form": form, "mensaje": "Información no válida"})

    else: #sino viene por GET y el formulario viene vacío
        formulario= CursoForm()
        return render (request, "AppCoder/cursoFormulario.html", {"form": formulario})

def profeFormulario(request):  # Creación de formulario
    if request.method=="POST":
        form= ProfeForm(request.POST) #por POST el formulario viene lleno
        
        if form.is_valid():
            informacion=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            
            nombre=informacion["nombre"]
            apellido=informacion["apellido"]
            email=informacion["email"]
            profesion=informacion["profesion"]            
            profe= Profesor(nombre=nombre, apellido=apellido, email= email, profesion=profesion)
            profe.save()
            profesores=Profesor.objects.all()
            return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores, "mensaje": "Profesor guardado correctamente"})
        else:
            return render (request, "AppCoder/profeFormulario.html", {"form": form, "mensaje": "Información no válida"})

    else: #sino viene por GET y el formulario viene vacío
        formulario= ProfeForm() #formulario vacío
        return render (request, "AppCoder/profeFormulario.html", {"form": formulario})

def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")

def buscar(request):
    
    comision=request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision) #Busca los cursos que corresponden a la comision que mandé por GET
        return render (request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render (request, "AppCoder/busquedaComision.html", {"mensaje": "Ingresa una comisión a buscar!"})

def leerProfesores(request):
    profesores=Profesor.objects.all()
    return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores})

def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado"})

def editarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form= ProfeForm(request.POST) #por POST el formulario viene lleno        
        if form.is_valid():
            info=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]     
            profesor.save()
            profesores=Profesor.objects.all()
            return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores, "mensaje": "Profesor editado correctamente"})
        pass
    else:
        formulario=ProfeForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email": profesor.email, "profesion": profesor.profesion})
        return render (request, "AppCoder/editarProfesor.html", {"form": formulario, "profesor": profesor})


#..........VISTAS BASADAS EN CLASES

class EstudianteList(ListView): #vista usada para LISTAR
    model=Estudiante #model que quiero mostrar
    template_name="AppCoder/estudiantes.html" #template que uso

class EstudianteCreacion(CreateView): #vista usada para CREAR
    model=Estudiante #model que quiero mostrar
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteUpdate(UpdateView): #vista usada para EDITAR
    model=Estudiante #model que quiero mostrar
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante #model que quiero mostrar
    template_name="AppCoder/estudiante_detalle.html" #template que uso

class EstudianteDelete(DeleteView): #vista usada para ELIMINAR
    model=Estudiante #model que quiero mostrar
    success_url= reverse_lazy("estudiante_list")

#................

def leerPersonas(request):
    personas=Persona.objects.all()
    return render (request, "AppCoder/leerPersonas.html", {"personas": personas})

def agregarPersona(request):
    if request.method=="POST":
        form= PersonaForm(request.POST) #por POST el formulario viene lleno
        
        if form.is_valid():
            informacion=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            
            nombre=informacion["nombre"]
            apellido=informacion["apellido"]
            dni=informacion["dni"]
            email=informacion["email"]
            fecha_nacimiento=informacion["fecha_nacimiento"]
            tieneObraSocial=informacion["tieneObraSocial"]            
            persona= Persona(nombre=nombre, apellido=apellido, dni=dni, email= email, fecha_nacimiento=fecha_nacimiento, tieneObraSocial=tieneObraSocial )
            persona.save()
            personas=Persona.objects.all()
            return render (request, "AppCoder/leerPersonas.html", {"personas": personas, "mensaje": "Persona guardada correctamente"})
        else:
            return render (request, "AppCoder/agregarPersona.html", {"form": form, "mensaje": "Información no válida"})

    else: #sino viene por GET y el formulario viene vacío
        form= PersonaForm() #formulario vacío
        return render (request, "AppCoder/agregarPersona.html", {"form": form})

def editarPersona(request, id):
    persona=Persona.objects.get(id=id)
    if request.method=="POST":
        form= PersonaForm(request.POST) #por POST el formulario viene lleno        
        if form.is_valid():
            info=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            persona.nombre=info["nombre"]
            persona.apellido=info["apellido"]
            persona.dni=info["dni"]
            persona.email=info["email"]
            persona.fecha_nacimiento=info["fecha_nacimiento"]
            persona.tieneObraSocial=info["tieneObraSocial"]           
            persona.save()
            personas=Persona.objects.all()
            return render (request, "AppCoder/leerPersonas.html", {"personas": personas, "mensaje": "Persona editada correctamente"})
        pass
    else:
        form=PersonaForm(initial={"nombre":persona.nombre, "apellido":persona.apellido, "dni": persona.dni, "email": persona.email, "fecha_nacimiento": persona.fecha_nacimiento})
        return render (request, "AppCoder/editarPersona.html", {"form": form, "persona": persona})

def eliminarPersona(request, id):
    persona=Persona.objects.get(id=id)
    persona.delete()
    personas=Persona.objects.all()
    return render (request, "AppCoder/leerPersonas.html", {"personas": personas, "mensaje": "Persona eliminada correctamente"})

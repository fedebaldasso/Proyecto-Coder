from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Persona, Avatar
from django.http import HttpResponse
from django.urls import reverse_lazy
from AppCoder.forms import CursoForm, ProfeForm, PersonaForm, RegistroUsuarioForm, UserEditForm, AvatarForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required #decorador para vistas basadas en funciones que permite que cambie un comportamiento cuando se está logueado
from django.contrib.auth.mixins import LoginRequiredMixin #decorador para vistas basadas en clases que permite que cambie un comportamiento cuando se está logueado


def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        avatar=lista[0].imagen.url
    else:
        avatar="/media/avatars/avatarpordefecto.png"
    return avatar


# Create your views here.

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def curso(request):
    cursito=Curso(nombre="Python", comision=34645)
    cursito.save()
    cadena_texto=f"curso guardado: Nombre {cursito.nombre}, Comision: {cursito.comision}"
    return HttpResponse(cadena_texto)

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def cursos(request):
    return render (request, "AppCoder/cursos.html")

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def estudiantes(request):
    return render (request, "AppCoder/estudiantes.html")

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def profesores(request):
    return render (request, "AppCoder/profesores.html")

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def entregables(request):
    return render (request, "AppCoder/entregables.html", {"avatar": obtenerAvatar(request)})

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

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
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

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
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

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def buscar(request):
    
    comision=request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision) #Busca los cursos que corresponden a la comision que mandé por GET
        return render (request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render (request, "AppCoder/busquedaComision.html", {"mensaje": "Ingresa una comisión a buscar!"})

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def leerProfesores(request):
    profesores=Profesor.objects.all() 
    return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores, "avatar": obtenerAvatar(request)})

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render (request, "AppCoder/leerProfesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado"})

@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
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

class EstudianteList(LoginRequiredMixin, ListView): #vista usada para LISTAR
    model=Estudiante #model que quiero mostrar
    template_name="AppCoder/estudiantes.html" #template que uso

class EstudianteCreacion(LoginRequiredMixin, CreateView): #vista usada para CREAR
    model=Estudiante #model que quiero mostrar
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteUpdate(LoginRequiredMixin, UpdateView): #vista usada para EDITAR
    model=Estudiante #model que quiero mostrar
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(LoginRequiredMixin, DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante #model que quiero mostrar
    template_name="AppCoder/estudiante_detalle.html" #template que uso

class EstudianteDelete(LoginRequiredMixin, DeleteView): #vista usada para ELIMINAR
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


#-------VISTA DE REGISTRO--------

def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST) #por POST el formulario viene lleno        
        if form.is_valid():
            username=form.cleaned_data.get("username") 
            form.save() #guardo en la base de datos el objeto que trae el formulario            
            return render (request, "AppCoder/inicio.html", {"mensaje": f"Usuario {username} creado correctamente"})
        else:
            return render (request, "AppCoder/register.html", {"form": form, "mensaje": "Error al crear el usuario"})

    else: #sino viene por GET y el formulario viene vacío
        form= RegistroUsuarioForm() #formulario vacío
        return render (request, "AppCoder/register.html", {"form": form})


#-------VISTA DE LOGIN--------

def login_request(request):  # Creación de formulario
    if request.method=="POST":
        form= AuthenticationForm(request, data = request.POST) #por POST el formulario viene lleno
        
        if form.is_valid():
            info=form.cleaned_data #convierte la info en modo formulario a un diccionario más facil de leer
            
            usuario=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usuario, password=clave) #verifica si el usuario existe, si existe, lo devuelve, y sino devuelve None
            if usuario is not None:
                login(request, usuario)            
                return render (request, "AppCoder/inicio.html", {"mensaje": f"Usuario {usuario} logueado correctamente"})
            else:
                return render (request, "AppCoder/login.html", {"form": form, "mensaje": "Usuario o Contraseña incorrectos"})

        else: #sino viene por GET y el formulario viene vacío
            return render (request, "AppCoder/login.html", {"form": form, "mensaje": "Usuario o Contraseña incorrectos"})
    else:
        form=AuthenticationForm()
        return render (request, "AppCoder/login.html", {"form": form})


@login_required #Solo permite acceder a la funcion y modificar lo que desee si estoy logueado
def editarPerfil(request):
    usuario=request.user

    if request.method=="POST":
        form= UserEditForm(request.POST) #por POST el formulario viene lleno        
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"] 
            usuario.first_name=info["first_name"] 
            usuario.last_name=info["last_name"]
            usuario.save() #guardo en la base de datos el objeto que trae el formulario            
            return render (request, "AppCoder/inicio.html", {"mensaje": f"Usuario {usuario.username} editado correctamente"})
        else:
            return render (request, "AppCoder/editarPerfil.html", {"form": form, "mensaje": "Error al editar el usuario"})

    else: #sino viene por GET y el formulario viene vacío
        form= UserEditForm(instance=usuario) #formulario vacío
        return render (request, "AppCoder/editarPerfil.html", {"form": form, "nombreusuario": usuario.username})

def agregarAvatar(request):
    if request.method=="POST":
        form= AvatarForm(request.POST, request.FILES) #por POST el formulario viene lleno        
        if form.is_valid():
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])
            avatarViejo=Avatar.objects.filter(user=request.user) #Se fija si ya tiene avatar y lo reemplaza por el nuevo
            if len(avatarViejo)>0:
                avatarViejo[0].delete()            
            avatar.save() #guardo en la base de datos el objeto que trae el formulario            
            return render (request, "AppCoder/inicio.html", {"mensaje": f"Avatar agregado correctamente"})
        else:
            return render (request, "AppCoder/agregarAvatar.html", {"form": form, "usuario":request.user, "mensaje": "Error al agregar el avatar"})

    else: #sino viene por GET y el formulario viene vacío
        form= AvatarForm() #formulario vacío
        return render (request, "AppCoder/agregarAvatar.html", {"form": form, "usuario": request.user})

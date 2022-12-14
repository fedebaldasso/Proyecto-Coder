from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Curso(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    comision=models.IntegerField() #lo defino como un entero de base de datos

    def __str__(self):
        return f"{self.nombre} - {str(self.comision)}"

class Estudiante(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    apellido=models.CharField(max_length=50) 
    email=models.EmailField()

    def __str__(self):
        return f"{self.nombre} {str(self.apellido)}"

class Profesor(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    apellido=models.CharField(max_length=50) #lo defino como un entero de base de datos
    email=models.EmailField()
    profesion= models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {str(self.apellido)}"

class Entregable(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    fecha_entrega=models.DateField()
    entregado=models.BooleanField()


class Persona(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    apellido=models.CharField(max_length=50) #lo defino como un entero de base de datos
    dni=models.IntegerField()
    email=models.EmailField()
    fecha_nacimiento=models.DateField()
    tieneObraSocial=models.BooleanField()

    def __str__(self):
        return f"{self.nombre} {str(self.apellido)}"

class Avatar(models.Model):
    imagen= models.ImageField(upload_to="avatars")
    user= models.ForeignKey(User, on_delete=models.CASCADE) #Hace la conexión del avatar con el usuario

    def __str__(self):
        return f"{self.user} {str(self.imagen)}"
    
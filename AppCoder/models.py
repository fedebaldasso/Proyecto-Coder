from django.db import models

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

class Profesor(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    apellido=models.CharField(max_length=50) #lo defino como un entero de base de datos
    email=models.EmailField()
    profesion= models.CharField(max_length=50)

class Entregable(models.Model):
    nombre= models.CharField(max_length=50) #lo defino como un caracter de base de datos
    fecha_entrega=models.DateField()
    entregado=models.BooleanField()

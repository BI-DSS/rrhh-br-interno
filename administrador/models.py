from __future__ import unicode_literals

from django.db import models
from solicitud.models import Solicitud, Departamento, Municipio
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Ofertas(models.Model):
    Cod_oferta = models.AutoField(primary_key=True, db_column='Cod_oferta')
    Puesto_oferta = models.CharField(max_length=600, blank=True, null=True, db_column='Puesto_oferta')
    Salario_minimo = models.IntegerField(blank=True, null=True, db_column='Salario_minimo')
    Salario_maximo = models.IntegerField(blank=True, null=True, db_column='Salario_maximo')
    Descripcion_oferta = models.TextField(blank=True, null=True, db_column='Descripcion_oferta')
    Perfil_candidato = models.TextField(blank=True, null=True, db_column='Perfil_candidato')
    Fecha_publicacion = models.DateField( blank=True, null=True, db_column='Fecha_publicacion')
    Fecha_cierre = models.DateField(blank=True, null=True, db_column='Fecha_cierre')
    Cod_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='Cod_departamento', blank=True, null=True) 
    Departamento = models.CharField(max_length=150, blank=True, null=True, db_column='Departemento')
    Cod_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='Cod_municipio', blank=True, null=True) 
    Municipio = models.CharField(max_length=150, blank=True, null=True, db_column='Municipio')
    Estado = models.NullBooleanField(db_column='Estado')
    Trabajo_campo = models.NullBooleanField(db_column='Trabajo_campo')
    Vehiculo = models.NullBooleanField(db_column='Vehiculo')
    Tipo_contratacion = models.CharField(max_length=150, blank=True, null=True, db_column='Tipo_contratacion')
    Edad_minima = models.IntegerField(blank=True, null=True, db_column='Edad_minima')
    Edad_maxima = models.IntegerField(blank=True, null=True, db_column='Edad_maxima')
    Disponibilidad = models.CharField(max_length=150, blank=True, null=True, db_column='Disponibilidad')
    Experiencia_laboral = models.CharField(max_length=150, blank=True, null=True, db_column='Experiencia_laboral')
    Cod_area = models.ForeignKey('Areas', models.DO_NOTHING, db_column='Cod_area', blank=True, null=True) 
    Descripcion_area = models.CharField(max_length=200, blank=True, null=True, db_column='Descripcion_area')
    Publica = models.NullBooleanField(db_column='Publica')
    Interna = models.NullBooleanField(db_column='Interna')
    Anonima = models.NullBooleanField(db_column='Anonima')
    Url = models.CharField(max_length=250, blank=True, null=True, db_column='Url')
    class Meta:
        managed = False
        db_table = 'Ofe].[Ofertas' 

class Preguntas(models.Model):
    Cod_pregunta = models.AutoField(primary_key=True, db_column='Cod_pregunta')
    Cod_oferta = models.ForeignKey('Ofertas', models.DO_NOTHING, db_column='Cod_oferta', blank=True, null=True) 
    Descripcion_pregunta = models.CharField(max_length=600, blank=True, null=True, db_column='Descripcion_pregunta')
    class Meta:
        managed = False
        db_table = 'Ofe].[Preguntas'

class Respuestas(models.Model):
    Cod_respuesta = models.AutoField(primary_key=True, db_column='Cod_respuesta')
    Cod_pregunta = models.ForeignKey('Preguntas', models.DO_NOTHING, db_column='Cod_pregunta', blank=True, null=True) 
    Cod_solicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)
    Cod_aplicacion = models.ForeignKey('Aplicaciones', models.DO_NOTHING, db_column='Cod_aplicacion', blank=True, null=True)
    Cod_oferta = models.ForeignKey('Ofertas', models.DO_NOTHING, db_column='Cod_oferta', blank=True, null=True)
    Descripcion_respuesta = models.TextField(blank=True, null=True, db_column='Descripcion_respuesta')
    Descripcion_pregunta = models.TextField(blank=True, null=True, db_column='Descripcion_pregunta')
    class Meta:
        managed = False
        db_table = 'Ofe].[Respuestas' 

class Aplicaciones(models.Model):
    Cod_aplicacion = models.AutoField(primary_key=True, db_column='Cod_aplicacion')
    Cod_oferta = models.ForeignKey('Ofertas', models.DO_NOTHING, db_column='Cod_oferta', blank=True, null=True) 
    Cod_solicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True) 
    Favorito = models.NullBooleanField(db_column='Favorito')
    Tipo_seguimiento = models.CharField(max_length=150, blank=True, null=True, db_column='Tipo_seguimiento')
    Visto = models.NullBooleanField(db_column='Visto')
    Dislike = models.NullBooleanField(db_column='Dislike')
    Imprimir = models.NullBooleanField(db_column='Imprimir')
    Fecha = models.DateField(db_column='Fecha', blank=True, null=True , default=timezone.now)
    codUser = models.ForeignKey(User, models.DO_NOTHING, db_column='CodUserDes', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Ofe].[Aplicaciones' 

class Areas(models.Model):
    Cod_area =models.AutoField(primary_key=True, db_column='Cod_area')
    Descripcion_area = models.CharField(max_length=200, blank=True, null=True, db_column='Descripcion_area')
    class Meta:
        managed = False
        db_table = 'Ofe].[Areas'

class TipoSeguimiento(models.Model):
    Cod_seguimiento =models.AutoField(primary_key=True, db_column='Cod_seguimiento')
    Descripcion_seguimiento = models.CharField(max_length=500, blank=True, null=True, db_column='Descripcion_seguimiento')
    class Meta:
        managed = False
        db_table = 'Ofe].[TipoSeguimiento'  


class SeguimientoXAplicacion(models.Model):
    Cod_Seguimiento = models.AutoField(primary_key=True, db_column='Cod_seguimiento')
    Cod_Oferta = models.ForeignKey('Ofertas', models.DO_NOTHING, db_column='Cod_oferta', blank=True, null=True) 
    Cod_Solicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True) 
    Cod_Aplicacion = models.ForeignKey('Aplicaciones', models.DO_NOTHING, db_column='Cod_aplicacion', blank=True, null=True)
    
    Pr_Entrevista = models.NullBooleanField(db_column='Pr_Entrevista')
    Fch_Pr_Entrevista = models.DateField(db_column='Fch_Pr_Entrevista', blank=True, null=True)
    Hor_Pr_Entrevista = models.DateTimeField(db_column='Hor_Pr_Entrevista', blank=True, null=True)
    
    Pruebas_Psico = models.NullBooleanField(db_column='Pruebas_Psico')
    Email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)
    Contrasena = models.CharField(db_column='Contrasena', max_length=50, blank=True, null=True)
    Fch_Pruebas_Psico = models.DateField(db_column='Fch_Pruebas_Psico', blank=True, null=True)
    
    Jefe_Inme = models.NullBooleanField(db_column='Jefe_Inme')
    Fch_Jefe = models.DateField(db_column='Fch_Jefe', blank=True, null=True)
    Hor_Jefe = models.DateTimeField(db_column='Hor_Jefe', blank=True, null=True)
   
    Poligrafo = models.NullBooleanField(db_column='Poligrafo')
    Fch_Poligrafo = models.DateField(db_column='Fch_Poligrafo', blank=True, null=True)
    Hor_Poligrafo = models.DateTimeField(db_column='Hor_Poligrafo', blank=True, null=True)
    Dir_Poligrafo = models.TextField(blank=True, null=True, db_column='Dir_Poligrafo')
    
    Socio_Econ = models.NullBooleanField(db_column='Socio_Econ')
    Fch_Socio = models.DateField(db_column='Fch_Socio', blank=True, null=True)
    Hor_Socio = models.DateTimeField(db_column='Hor_Socio', blank=True, null=True)
    
    Documentacion = models.NullBooleanField(db_column='Documentacion')
    Fch_Doc = models.DateField(db_column='Fch_Doc', blank=True, null=True)
   
    Medicos = models.NullBooleanField(db_column='Medicos')
    Fch_Medicos = models.DateField(db_column='Fch_Medicos', blank=True, null=True)
    Hor_Medicos = models.DateTimeField(db_column='Hor_Medicos', blank=True, null=True)
    Dir_Medicos = models.TextField(blank=True, null=True, db_column='Dir_Medicos')
    CC = models.NullBooleanField(db_column='CC')
    Fch_Ingreso = models.DateField(db_column='Fch_Ingreso', blank=True, null=True)
    Fch_Salida = models.DateField(db_column='Fch_Salida', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Ofe].[SeguimientoXAplicacion'


class Suscriptores(models.Model):
    Cod_suscripcion =models.AutoField(primary_key=True, db_column='Cod_suscripcion')
    Cod_area = models.ForeignKey('Areas', models.DO_NOTHING, db_column='Cod_area', blank=True, null=True) 
    Correo = models.CharField(max_length=300, blank=True, null=True, db_column='Correo')
    Estado = models.NullBooleanField(db_column='Estado')
    class Meta:
        managed = False
        db_table = 'Ofe].[Suscriptores'
            


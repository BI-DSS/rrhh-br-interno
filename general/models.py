from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from solicitud.models import Departamento, Municipio
import uuid

class Perfil(models.Model):
    cod_usuario = models.AutoField(primary_key=True, db_column='cod_usuario')
    nombre_usuario = models.CharField(max_length=200, blank=True, null=True, db_column='nombre_usuario')
    apellido_usuario = models.CharField(max_length=200, blank=True, null=True, db_column='apellido_usuario')
    cod_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='cod_departamento', blank=True, null=True)
    cod_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='cod_municipio', blank=True, null=True)
    sexo_usuario = models.CharField(max_length=1, blank=True, null=True, db_column='sexo_usuario')
    correo_usuario = models.CharField(max_length=50, blank=True, null=True, db_column='correo_usuario')
    direccion_usuario = models.CharField(max_length=300, blank=True, null=True, db_column='direccion_usuario')
    fecha_nacimiento = models.CharField(max_length=10, blank=True, null=True, db_column='fecha_nacimiento')
    telefono_celular = models.CharField(max_length=10, blank=True, null=True, db_column='telefono_celular')
    telefono_fijo = models.CharField(max_length=10, blank=True, null=True, db_column='telefono_fijo')
    telefono_oficina = models.IntegerField(blank=True, null=True, db_column='telefono_oficina')
    vehiculo = models.NullBooleanField(db_column='vehiculo')
    licencia = models.NullBooleanField(db_column='licencia')
    estado = models.NullBooleanField(db_column='estado')
    cod_user = models.ForeignKey(User, models.DO_NOTHING, db_column='cod_user', blank=True, null=True)
    foto_usuario = models.ImageField(upload_to='fotos/')
 
    class Meta:
        managed = False
        db_table = 'Perfil'

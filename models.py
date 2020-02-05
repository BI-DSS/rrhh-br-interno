<<<<<<< HEAD
=======
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
>>>>>>> arwy18
from __future__ import unicode_literals

from django.db import models


class Campus(models.Model):
<<<<<<< HEAD
    cod_campus = models.AutoField(db_column='Cod_campus', primary_key=True)  # Field name made lowercase.
=======
    cod_campus = models.IntegerField(db_column='Cod_campus', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_universidad = models.ForeignKey('Universidades', models.DO_NOTHING, db_column='Cod_universidad', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Campus'


class Carreras(models.Model):
    cod_carreras = models.AutoField(db_column='Cod_carreras', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Campus'


class Carreras(models.Model):
    cod_carreras = models.IntegerField(db_column='Cod_carreras', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='Cod_campus', blank=True, null=True)  # Field name made lowercase.
    nombre_carrera = models.CharField(db_column='Nombre_carrera', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Carreras'
=======
        db_table = 'Carreras'
>>>>>>> arwy18


class CarrerasSolicitud(models.Model):
    cod_solicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='Cod_solicitud')  # Field name made lowercase.
    cod_universidad = models.IntegerField(db_column='Cod_universidad')  # Field name made lowercase.
    cod_campus = models.IntegerField(db_column='Cod_campus')  # Field name made lowercase.
    cod_carrera = models.ForeignKey(Carreras, models.DO_NOTHING, db_column='Cod_carrera')  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Carreras_Solicitud'
=======
        db_table = 'Carreras_Solicitud'
>>>>>>> arwy18
        unique_together = (('cod_solicitud', 'cod_carrera'),)


class Colegios(models.Model):
<<<<<<< HEAD
    cod_colegios = models.AutoField(db_column='Cod_Colegios', primary_key=True)  # Field name made lowercase.
=======
    cod_colegios = models.IntegerField(db_column='Cod_Colegios', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    nombre = models.CharField(db_column='Nombre', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Colegios'


class Competencias(models.Model):
    cod_compentencias = models.AutoField(db_column='Cod_compentencias', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Colegios'


class Competencias(models.Model):
    cod_compentencias = models.IntegerField(db_column='Cod_compentencias', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_solicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre_competencia = models.CharField(db_column='Nombre_competencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posee = models.NullBooleanField(db_column='Posee')  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Competencias'


class Cuentas(models.Model):
    cod_cuenta = models.AutoField(db_column='Cod_cuenta', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Competencias'


class Cuentas(models.Model):
    cod_cuenta = models.IntegerField(db_column='Cod_cuenta', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_solicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    tipo_cuenta = models.CharField(db_column='Tipo_cuenta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    institucion = models.CharField(db_column='Institucion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numero_cuenta = models.CharField(db_column='Numero_cuenta', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Cuentas'


class Cursos(models.Model):
    codcurso = models.AutoField(db_column='CodCurso', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Cuentas'


class Cursos(models.Model):
    codcurso = models.IntegerField(db_column='CodCurso', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    temacurso = models.CharField(db_column='TemaCurso', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nombrecentroestudio = models.CharField(db_column='NombreCentroEstudio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccioncentroestudio = models.CharField(db_column='DireccionCentroEstudio', max_length=150, blank=True, null=True)  # Field name made lowercase.
    duracion = models.CharField(db_column='Duracion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Cursos'


class Departamentos(models.Model):
    coddepartamento = models.AutoField(db_column='CodDepartamento', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Cursos'


class Departamentos(models.Model):
    coddepartamento = models.IntegerField(db_column='CodDepartamento', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codpais = models.ForeignKey('Paises', models.DO_NOTHING, db_column='CodPais', blank=True, null=True)  # Field name made lowercase.
    descripciondepartamento = models.CharField(db_column='DescripcionDepartamento', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Departamentos'


class Dependientes(models.Model):
    coddependiente = models.AutoField(db_column='CodDependiente', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Departamentos'


class Dependientes(models.Model):
    coddependiente = models.IntegerField(db_column='CodDependiente', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipodependencia = models.CharField(db_column='TipoDependencia', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Dependientes'
=======
        db_table = 'Dependientes'
>>>>>>> arwy18


class Escuelas(models.Model):
    cod_escuelas = models.IntegerField(db_column='Cod_escuelas', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Escuelas'


class Habilidades(models.Model):
    cod_habilidad = models.AutoField(db_column='Cod_habilidad', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Escuelas'


class GrupoOrganizacion(models.Model):
    cod_organizaciones = models.IntegerField(db_column='Cod_organizaciones', primary_key=True)  # Field name made lowercase.
    nombre_organizacion = models.CharField(db_column='Nombre_organizacion', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Grupo_organizacion'


class Habilidades(models.Model):
    cod_habilidad = models.IntegerField(db_column='Cod_habilidad', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_solicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre_habilidad = models.CharField(db_column='Nombre_habilidad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.IntegerField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Habilidades'


class Hermanos(models.Model):
    codhermano = models.AutoField(db_column='CodHermano', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Habilidades'


class Hermanos(models.Model):
    codhermano = models.IntegerField(db_column='CodHermano', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    domicilio = models.CharField(db_column='Domicilio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ocupacion = models.CharField(db_column='Ocupacion', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Hermanos'


class Hijos(models.Model):
    codhijo = models.AutoField(db_column='CodHijo', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Hermanos'


class Hijos(models.Model):
    codhijo = models.IntegerField(db_column='CodHijo', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Hijos'


class Historialacademico(models.Model):
    codinstitucion = models.AutoField(db_column='CodInstitucion', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Hijos'


class Historialacademico(models.Model):
    codinstitucion = models.IntegerField(db_column='CodInstitucion', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombreinstitucion = models.CharField(db_column='NombreInstitucion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    estudiosrealizados = models.CharField(db_column='EstudiosRealizados', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lugarestudio = models.CharField(db_column='LugarEstudio', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaestudio = models.CharField(db_column='FechaEstudio', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tituloobtenido = models.CharField(db_column='TituloObtenido', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[HistorialAcademico'


class Historiallaboral(models.Model):
    codempresa = models.AutoField(db_column='CodEmpresa', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'HistorialAcademico'


class Historiallaboral(models.Model):
    codempresa = models.IntegerField(db_column='CodEmpresa', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombreempresa = models.CharField(db_column='NombreEmpresa', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaINgreso', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaegreso = models.CharField(db_column='FechaEgreso', max_length=10, blank=True, null=True)  # Field name made lowercase.
    direccionempresa = models.CharField(db_column='DireccionEmpresa', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nombrejefeinmediato = models.CharField(db_column='NombreJefeInmediato', max_length=100, blank=True, null=True)  # Field name made lowercase.
    motivoretiro = models.CharField(db_column='MotivoRetiro', max_length=100, blank=True, null=True)  # Field name made lowercase.
    salarioinicial = models.DecimalField(db_column='SalarioInicial', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salariofinal = models.DecimalField(db_column='SalarioFinal', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='Puesto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fucionespuesto = models.CharField(db_column='FucionesPuesto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[HistorialLaboral'


class Idiomas(models.Model):
    cod_idioma = models.AutoField(db_column='Cod_idioma', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'HistorialLaboral'


class Idiomas(models.Model):
    cod_idioma = models.IntegerField(db_column='Cod_idioma', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_solicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    habla = models.IntegerField(db_column='Habla', blank=True, null=True)  # Field name made lowercase.
    escritura = models.IntegerField(db_column='Escritura', blank=True, null=True)  # Field name made lowercase.
    lectura = models.IntegerField(db_column='Lectura', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Idiomas'


class Municipios(models.Model):
    codmunicipio = models.AutoField(db_column='CodMunicipio', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Idiomas'


class Municipios(models.Model):
    codmunicipio = models.IntegerField(db_column='CodMunicipio', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    coddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
    descripcionmunicipio = models.CharField(db_column='DescripcionMunicipio', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Municipios'


class Organiacion(models.Model):
    cod_organizacion = models.AutoField(db_column='Cod_organizacion', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Municipios'


class Organiacion(models.Model):
    cod_organizacion = models.IntegerField(db_column='Cod_organizacion', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_solicitud = models.IntegerField(db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Organiacion'


class Paises(models.Model):
    codpais = models.AutoField(db_column='CodPais', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Organiacion'


class Paises(models.Model):
    codpais = models.IntegerField(db_column='CodPais', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    descripcionpais = models.CharField(db_column='DescripcionPais', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Paises'


class Referencias(models.Model):
    codreferencia = models.AutoField(db_column='CodReferencia', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Paises'


class Perfil(models.Model):
    cod_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=200, blank=True, null=True)
    apellido_usuario = models.CharField(max_length=200, blank=True, null=True)
    cod_departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='cod_departamento', blank=True, null=True)
    cod_municipio = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='cod_municipio', blank=True, null=True)
    sexo_usuario = models.CharField(max_length=1, blank=True, null=True)
    correo_usuario = models.CharField(max_length=50, blank=True, null=True)
    direccion_usuario = models.CharField(max_length=300, blank=True, null=True)
    fecha_nacimiento = models.CharField(max_length=10, blank=True, null=True)
    telefono_celular = models.IntegerField(blank=True, null=True)
    telefono_fijo = models.IntegerField(blank=True, null=True)
    telefono_oficina = models.IntegerField(blank=True, null=True)
    vehiculo = models.NullBooleanField()
    licencia = models.NullBooleanField()
    estado = models.NullBooleanField()
    cod_user = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='cod_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Perfil'


class Referencias(models.Model):
    codreferencia = models.IntegerField(db_column='CodReferencia', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tiporeferencia = models.CharField(db_column='TipoReferencia', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Referencias'


class Referenciaspersonales(models.Model):
    codreferenciapersonal = models.AutoField(db_column='CodReferenciaPersonal', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'Referencias'


class Referenciaspersonales(models.Model):
    codreferenciapersonal = models.IntegerField(db_column='CodReferenciaPersonal', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    codsolicitud = models.ForeignKey('Solicitudes', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[ReferenciasPersonales'


class Solicitudes(models.Model):
    codsolicitud = models.AutoField(db_column='CodSolicitud', primary_key=True)  # Field name made lowercase.
=======
        db_table = 'ReferenciasPersonales'


class Solicitudes(models.Model):
    codsolicitud = models.IntegerField(db_column='CodSolicitud', primary_key=True)  # Field name made lowercase.
>>>>>>> arwy18
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    vista = models.IntegerField(db_column='Vista', blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=100, blank=True, null=True)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=100, blank=True, null=True)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    casada = models.NullBooleanField(db_column='Casada')  # Field name made lowercase.
    apellidocasada = models.CharField(db_column='ApellidoCasada', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direcciondomicilio = models.CharField(db_column='DireccionDomicilio', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codmunicipiodomicilio = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='CodMunicipioDomicilio', blank=True, null=True)  # Field name made lowercase.
    coddepartamentodomicilio = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='CodDepartamentoDomicilio', blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lugarnacimiento = models.CharField(db_column='LugarNacimiento', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechanacimiento = models.CharField(db_column='FechaNacimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    estadocivil = models.CharField(db_column='EstadoCivil', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codpaisnacimiento = models.ForeignKey(Paises, models.DO_NOTHING, db_column='CodPaisNacimiento', blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    identidad = models.CharField(db_column='Identidad', max_length=13, blank=True, null=True)  # Field name made lowercase.
    codmunicipioidentidad = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='CodMunicipioIdentidad', blank=True, null=True)  # Field name made lowercase.
    automovil = models.NullBooleanField(db_column='Automovil')  # Field name made lowercase.
    licencia = models.NullBooleanField(db_column='Licencia')  # Field name made lowercase.
    tipolicencia = models.CharField(db_column='TipoLicencia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    polizaseguro = models.NullBooleanField(db_column='PolizaSeguro')  # Field name made lowercase.
    companiapoliza = models.CharField(db_column='CompaniaPoliza', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deporte = models.NullBooleanField(db_column='Deporte')  # Field name made lowercase.
    tipodeporte = models.CharField(db_column='TipoDeporte', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechadeporte = models.CharField(db_column='FechaDeporte', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numeroihss = models.CharField(db_column='NumeroIhss', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rtn = models.CharField(db_column='RTN', max_length=14, blank=True, null=True)  # Field name made lowercase.
    numeropasaporte = models.CharField(db_column='NumeroPasaporte', max_length=50, blank=True, null=True)  # Field name made lowercase.
    organizaciones = models.CharField(db_column='Organizaciones', max_length=250, blank=True, null=True)  # Field name made lowercase.
    nombrespadre = models.CharField(db_column='NombresPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidospadre = models.CharField(db_column='ApellidosPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadpadre = models.IntegerField(db_column='EdadPadre', blank=True, null=True)  # Field name made lowercase.
    domiciliopadre = models.CharField(db_column='DomicilioPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefonopadre = models.CharField(db_column='TelefonoPadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionpadre = models.CharField(db_column='ProfesionPadre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralpadre = models.CharField(db_column='DireccionLaboralPadre', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nombresmadre = models.CharField(db_column='NombresMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidosmadre = models.CharField(db_column='ApellidosMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadmadre = models.IntegerField(db_column='EdadMadre', blank=True, null=True)  # Field name made lowercase.
    domiciliomadre = models.CharField(db_column='DomicilioMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefonomadre = models.CharField(db_column='TelefonoMadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionmadre = models.CharField(db_column='ProfesionMadre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralmadre = models.CharField(db_column='DireccionLaboralMadre', max_length=200, blank=True, null=True)  # Field name made lowercase.
    hermanos = models.NullBooleanField(db_column='Hermanos')  # Field name made lowercase.
    cantidadhermanos = models.IntegerField(db_column='CantidadHermanos', blank=True, null=True)  # Field name made lowercase.
    cantidadhijos = models.IntegerField(db_column='CantidadHijos', blank=True, null=True)  # Field name made lowercase.
    cantidaddependientes = models.IntegerField(db_column='CantidadDependientes', blank=True, null=True)  # Field name made lowercase.
    nombreconyugue = models.CharField(db_column='NombreConyugue', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadconyugue = models.IntegerField(db_column='EdadConyugue', blank=True, null=True)  # Field name made lowercase.
    domicilioconyugue = models.CharField(db_column='DomicilioConyugue', max_length=200, blank=True, null=True)  # Field name made lowercase.
    telefonoconyugue = models.CharField(db_column='TelefonoConyugue', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionconyugue = models.CharField(db_column='ProfesionConyugue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralconyugue = models.CharField(db_column='DireccionLaboralConyugue', max_length=200, blank=True, null=True)  # Field name made lowercase.
    tipovivienda = models.CharField(db_column='TipoVivienda', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalamortizacion = models.DecimalField(db_column='TotalAmortizacion', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalinquilino = models.DecimalField(db_column='TotalInquilino', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalpensionista = models.DecimalField(db_column='TotalPensionista', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    deudaspendientes = models.DecimalField(db_column='DeudasPendientes', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nombreacreedor = models.CharField(db_column='NombreAcreedor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    montodeuda = models.DecimalField(db_column='MontoDeuda', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cuotamensual = models.DecimalField(db_column='CuotaMensual', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    embargado = models.NullBooleanField(db_column='Embargado')  # Field name made lowercase.
    nombrequienembargo = models.CharField(db_column='NombreQuienEmbargo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    motivoembargo = models.CharField(db_column='MotivoEmbargo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    montoembargo = models.DecimalField(db_column='MontoEmbargo', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    valoresefectivo = models.NullBooleanField(db_column='ValoresEfectivo')  # Field name made lowercase.
    montoefectivo = models.DecimalField(db_column='MontoEfectivo', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    familiaresinstitucion = models.NullBooleanField(db_column='FamiliaresInstitucion')  # Field name made lowercase.
    nombrefamiliar = models.CharField(db_column='NombreFamiliar', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parentesco = models.CharField(db_column='Parentesco', max_length=1, blank=True, null=True)  # Field name made lowercase.
    puestofamiliar = models.CharField(db_column='PuestoFamiliar', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trabajarcualquierlugar = models.NullBooleanField(db_column='TrabajarCualquierLugar')  # Field name made lowercase.
    nombrequienrecomienda = models.CharField(db_column='NombreQuienRecomienda', max_length=100, blank=True, null=True)  # Field name made lowercase.
    puestoquesolicita = models.CharField(db_column='PuestoQueSolicita', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sueldopretende = models.DecimalField(db_column='SueldoPretende', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.CharField(db_column='FechaInicio', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enfermedadeshapadecido = models.CharField(db_column='EnfermedadesHaPadecido', max_length=200, blank=True, null=True)  # Field name made lowercase.
    consumemedicamentos = models.NullBooleanField(db_column='ConsumeMedicamentos')  # Field name made lowercase.
    impedimentosfisicos = models.NullBooleanField(db_column='ImpedimentosFisicos')  # Field name made lowercase.
    observacionesadicionales = models.CharField(db_column='ObservacionesAdicionales', max_length=200, blank=True, null=True)  # Field name made lowercase.
<<<<<<< HEAD
    cod_colegio = models.ForeignKey(Colegios, models.DO_NOTHING, db_column='Cod_colegio', blank=True, null=True)  # Field name made lowercase.
=======
    cod_colegio = models.ForeignKey(Organiacion, models.DO_NOTHING, db_column='Cod_colegio', blank=True, null=True)  # Field name made lowercase.
>>>>>>> arwy18
    cod_escuela = models.ForeignKey(Escuelas, models.DO_NOTHING, db_column='Cod_Escuela', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Solicitudes'
=======
        db_table = 'Solicitudes'
>>>>>>> arwy18


class Universidades(models.Model):
    cod_univesidad = models.IntegerField(db_column='Cod_univesidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
<<<<<<< HEAD
        db_table = 'Sol].[Universidades'

=======
        db_table = 'Universidades'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
>>>>>>> arwy18

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Campus(models.Model):
    cod_campus = models.AutoField(db_column='Cod_campus', primary_key=True)  # Field name made lowercase.
    cod_universidad = models.ForeignKey('Universidad', models.DO_NOTHING, db_column='Cod_universidad', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Campus'


class Carrera(models.Model):
    cod_carreras = models.AutoField(db_column='Cod_carreras', primary_key=True)  # Field name made lowercase.
    cod_campus = models.ForeignKey('Universidad', models.DO_NOTHING, db_column='Cod_campus', blank=True, null=True)  # Field name made lowercase.
    nombre_carrera = models.CharField(db_column='Nombre_carrera', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Carreras'


class CarrerasSolicitud(models.Model):
    cod_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='Cod_solicitud')  # Field name made lowercase.
    cod_universidad = models.IntegerField(db_column='Cod_universidad')  # Field name made lowercase.
    cod_campus = models.IntegerField(db_column='Cod_campus')  # Field name made lowercase.
    cod_carrera = models.ForeignKey(Carrera, models.DO_NOTHING, db_column='Cod_carrera')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Carreras_Solicitud'
        unique_together = (('cod_solicitud', 'cod_carrera'),)


class Colegio(models.Model):
    cod_colegios = models.AutoField(db_column='Cod_Colegios', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Colegios'


class Competencia(models.Model):
    cod_compentencias = models.AutoField(db_column='Cod_compentencias', primary_key=True)  # Field name made lowercase.
    cod_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre_competencia = models.CharField(db_column='Nombre_competencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posee = models.NullBooleanField(db_column='Posee')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Competencias'


class Cuenta(models.Model):
    cod_cuenta = models.AutoField(db_column='Cod_cuenta', primary_key=True)  # Field name made lowercase.
    cod_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    tipo_cuenta = models.CharField(db_column='Tipo_cuenta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    institucion = models.CharField(db_column='Institucion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numero_cuenta = models.TextField(db_column='Numero_cuenta', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Sol].[Cuentas'


class Curso(models.Model):
    codcurso = models.AutoField(db_column='CodCurso', primary_key=True)  # Field name made lowercase.
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    temacurso = models.CharField(db_column='TemaCurso', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nombrecentroestudio = models.CharField(db_column='NombreCentroEstudio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccioncentroestudio = models.TextField(db_column='DireccionCentroEstudio', blank=True, null=True)  # Field name made lowercase.
    duracion = models.CharField(db_column='Duracion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Cursos'

 
class Departamento(models.Model):
    coddepartamento = models.AutoField(db_column='CodDepartamento', primary_key=True)  # Field name made lowercase.
    codpais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='CodPais', blank=True, null=True)  # Field name made lowercase.
    descripciondepartamento = models.CharField(db_column='DescripcionDepartamento', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Departamentos'

class Dependiente(models.Model):
    coddependiente = models.AutoField(db_column='CodDependiente', primary_key=True)  # Field name made lowercase.
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombredependiente = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipodependencia = models.CharField(db_column='TipoDependencia', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Dependientes'

class Escuela(models.Model):
    cod_escuelas = models.IntegerField(db_column='Cod_escuelas', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Escuelas'

class Habilidad(models.Model):
    cod_habilidad = models.AutoField(db_column='Cod_habilidad', primary_key=True)  # Field name made lowercase.
    cod_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre_habilidad = models.CharField(db_column='Nombre_habilidad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.IntegerField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Habilidades'

class Hermano(models.Model):
    codhermano = models.AutoField(db_column='CodHermano', primary_key=True)  # Field name made lowercase.
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', related_name="hermano_solicitud", blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    domicilio = models.TextField(db_column='Domicilio',  blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ocupacion = models.CharField(db_column='Ocupacion', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Hermanos'

class Hijo(models.Model):
    codhijo = models.AutoField(db_column='CodHijo', primary_key=True)  # Field name made lowercase.
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombreshijo = models.CharField(db_column='Nombres', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidoshijo = models.CharField(db_column='Apellidos', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadhijo = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Hijos'

class Historialacademico(models.Model):
    codinstitucion = models.AutoField(db_column='CodInstitucion', primary_key=True)
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombreinstitucion = models.CharField(db_column='NombreInstitucion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nivelestudios = models.CharField(db_column='NivelEstudios', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lugarestudio = models.CharField(db_column='LugarEstudio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tituloobtenido = models.CharField(db_column='TituloObtenido', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inicio = models.IntegerField(db_column='Inicio', null=True, blank=True)
    fin = models.IntegerField(db_column='Fin', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Sol].[HistorialAcademico'
  
class Historiallaboral(models.Model):
    codempresa = models.AutoField(db_column='CodEmpresa', primary_key=True)
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombreempresa = models.CharField(db_column='NombreEmpresa', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaINgreso', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaegreso = models.CharField(db_column='FechaEgreso', max_length=10, blank=True, null=True)  # Field name made lowercase.
    direccionempresa = models.TextField(db_column='DireccionEmpresa', blank=True, null=True)  # Field name made lowercase.
    nombrejefeinmediato = models.CharField(db_column='NombreJefeInmediato', max_length=100, blank=True, null=True)  # Field name made lowercase.
    motivoretiro = models.CharField(db_column='MotivoRetiro', max_length=100, blank=True, null=True)  # Field name made lowercase.
    salarioinicial = models.DecimalField(db_column='SalarioInicial', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salariofinal = models.DecimalField(db_column='SalarioFinal', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='Puesto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fucionespuesto = models.CharField(db_column='FucionesPuesto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=100, blank=True, null=True)  # Field name made lowercase.
    horainicio = models.CharField(db_column='HoraInicio',  max_length=50 , blank=True, null=True)
    horasalida = models.CharField(db_column='HoraSalida',  max_length=50 , blank=True, null=True)
    sabado = models.NullBooleanField(db_column='Sabado')
    horainiciosabado = models.CharField(db_column='HoraInicioSabado', max_length=50 , blank=True, null=True)
    horasalidasabado = models.CharField(db_column='HoraSalidaSabado',  max_length=50 , blank=True, null=True)
    trabajoactual = models.NullBooleanField(db_column='TrabajoActual')

    class Meta:
        managed = False
        db_table = 'Sol].[HistorialLaboral'

class Idioma(models.Model):
    cod_idioma = models.AutoField(db_column='Cod_idioma', primary_key=True)  # Field name made lowercase.
    cod_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    habla = models.IntegerField(db_column='Habla', blank=True, null=True)  # Field name made lowercase.
    escritura = models.IntegerField(db_column='Escritura', blank=True, null=True)  # Field name made lowercase.
    lectura = models.IntegerField(db_column='Lectura', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Idiomas'

class Municipio(models.Model):
    codmunicipio = models.AutoField(db_column='CodMunicipio', primary_key=True)  # Field name made lowercase.
    coddepartamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
    descripcionmunicipio = models.CharField(db_column='DescripcionMunicipio', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sol].[Municipios'

class Grupo_organizacion(models.Model):
    cod_organizaciones = models.AutoField(db_column='Cod_organizaciones', primary_key=True)  # Field name made lowercase.
    nombre_organizacion = models.CharField(db_column='Nombre_organizacion', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Grupo_organizacion'

class Organizacion(models.Model):
    cod_organizacion = models.AutoField(db_column='Cod_organizacion', primary_key=True)  # Field name made lowercase.
    cod_solicitud = models.IntegerField(db_column='Cod_solicitud', blank=True, null=True)  # Field name made lowercase.
    cod_grupo_organizacion = models.IntegerField(db_column='CodGrupoOrganizacion', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Organiacion'

class Pais(models.Model):
    codpais = models.AutoField(db_column='CodPais', primary_key=True)  # Field name made lowercase.
    descripcionpais = models.CharField(db_column='DescripcionPais', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Paises'

    def __unicode__(self):
        return self.descripcionpais

class Referencia(models.Model):
    codreferencia = models.AutoField(db_column='CodReferencia', primary_key=True)
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion = models.TextField(db_column='Direccion',  blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Referencias'

class Referenciaspersonal(models.Model):
    codreferenciapersonal = models.AutoField(db_column='CodReferenciaPersonal', primary_key=True)  # Field name made lowercase.
    codsolicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='CodSolicitud', blank=True, null=True)  # Field name made lowercase.
    nombre_personal = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion_personal = models.CharField(db_column='Profesion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion_personal = models.TextField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    telefono_personal = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[ReferenciasPersonales'

class Seguros(models.Model):
    cod_seguros = models.AutoField(db_column='CodSeguros', primary_key=True)
    compania_seguros = models.CharField(db_column='CompaniaSeguros', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguros'

def directorio_upload(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.cod_user, filename.encode('ascii', 'ignore'))

# def directorio_upload(instance, filename):
#  # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'uploads/user_{0}/{1}/{2}'.format(instance.creado_por, instance.__class__.__name__, filename.encode('ascii', 'ignore'))
  
class Solicitud(models.Model):
    codsolicitud = models.AutoField(db_column='CodSolicitud', primary_key=True)  # Field name made lowercase.
    cod_user = models.ForeignKey(User, db_column='CodUser', blank=True, null=True)
    correo = models.CharField(db_column='Correo', max_length=200, blank=True, null=True)
    foto_usuario = models.ImageField(upload_to='fotos/')
    anonima = models.NullBooleanField(db_column='Anonima')
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    vista = models.IntegerField(db_column='Vista', blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=100, blank=True, null=True)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=100, blank=True, null=True)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    casada = models.NullBooleanField(db_column='Casada')  # Field name made lowercase.
    apellidocasada = models.CharField(db_column='ApellidoCasada', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direcciondomicilio = models.TextField(db_column='DireccionDomicilio', blank=True, null=True)  # Field name made lowercase.
    codmunicipiodomicilio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='CodMunicipioDomicilio', related_name="cod_municipios", blank=True, null=True)  # Field name made lowercase.
    coddepartamentodomicilio = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='CodDepartamentoDomicilio', blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lugarnacimiento = models.CharField(db_column='LugarNacimiento', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechanacimiento = models.CharField(db_column='FechaNacimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    estadocivil = models.CharField(db_column='EstadoCivil', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codpaisnacimiento = models.ForeignKey(Pais, models.DO_NOTHING, db_column='CodPaisNacimiento', blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    identidad = models.CharField(db_column='Identidad', max_length=15, blank=True, null=True)  # Field name made lowercase.
    codmunicipioidentidad = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='CodMunicipioIdentidad', blank=True, null=True)  # Field name made lowercase.
    automovil = models.NullBooleanField(db_column='Automovil')  # Field name made lowercase.
    licencia = models.NullBooleanField(db_column='Licencia')  # Field name made lowercase.
    liviana = models.NullBooleanField(db_column='Liviana')  # Field name made lowercase.
    pesada = models.NullBooleanField(db_column='Pesada')  # Field name made lowercase.
    motocicleta = models.NullBooleanField(db_column='Motocicleta')  # Field name made lowercase.
    polizaseguro = models.NullBooleanField(db_column='PolizaSeguro')  # Field name made lowercase.
    companiapoliza = models.CharField(db_column='CompaniaPoliza', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deporte = models.NullBooleanField(db_column='Deporte')  # Field name made lowercase.
    tipodeporte = models.CharField(db_column='TipoDeporte', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechadeporte = models.CharField(db_column='FechaDeporte', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numeroihss = models.CharField(db_column='NumeroIhss', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rtn = models.CharField(db_column='RTN', max_length=16, blank=True, null=True)  # Field name made lowercase.
    numeropasaporte = models.CharField(db_column='NumeroPasaporte', max_length=50, blank=True, null=True)  # Field name made lowercase.
    organizaciones = models.CharField(db_column='Organizaciones', max_length=250, blank=True, null=True)  # Field name made lowercase.
    nombrespadre = models.CharField(db_column='NombresPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidospadre = models.CharField(db_column='ApellidosPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadpadre = models.IntegerField(db_column='EdadPadre', blank=True, null=True)  # Field name made lowercase.
    domiciliopadre = models.TextField(db_column='DomicilioPadre', blank=True, null=True)  # Field name made lowercase.
    telefonopadre = models.CharField(db_column='TelefonoPadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    celularpadre = models.CharField(db_column='CelularPadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionpadre = models.CharField(db_column='ProfesionPadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralpadre = models.TextField(db_column='DireccionLaboralPadre', blank=True, null=True)  # Field name made lowercase.
    nombresmadre = models.CharField(db_column='NombresMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidosmadre = models.CharField(db_column='ApellidosMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadmadre = models.IntegerField(db_column='EdadMadre', blank=True, null=True)  # Field name made lowercase.
    domiciliomadre = models.TextField(db_column='DomicilioMadre', blank=True, null=True)  # Field name made lowercase.
    telefonomadre = models.CharField(db_column='TelefonoMadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    celularmadre = models.CharField(db_column='CelularMadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionmadre = models.CharField(db_column='ProfesionMadre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralmadre = models.TextField(db_column='DireccionLaboralMadre', blank=True, null=True)  # Field name made lowercase.
    hermanos = models.NullBooleanField(db_column='Hermanos')  # Field name made lowercase.
    cantidadhermanos = models.IntegerField(db_column='CantidadHermanos', blank=True, null=True)  # Field name made lowercase.
    cantidadhijos = models.IntegerField(db_column='CantidadHijos', blank=True, null=True)  # Field name made lowercase.
    cantidaddependientes = models.IntegerField(db_column='CantidadDependientes', blank=True, null=True)  # Field name made lowercase.
    nombreconyugue = models.CharField(db_column='NombreConyugue', max_length=100, blank=True, null=True)  # Field name made lowercase.
    edadconyugue = models.IntegerField(db_column='EdadConyugue', blank=True, null=True)  # Field name made lowercase.
    domicilioconyugue = models.TextField(db_column='DomicilioConyugue', blank=True, null=True)  # Field name made lowercase.
    telefonoconyugue = models.CharField(db_column='TelefonoConyugue', max_length=10, blank=True, null=True)  # Field name made lowercase.
    profesionconyugue = models.CharField(db_column='ProfesionConyugue', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccionlaboralconyugue = models.TextField(db_column='DireccionLaboralConyugue', blank=True, null=True)  # Field name made lowercase.
    tipovivienda = models.CharField(db_column='TipoVivienda', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalamortizacion = models.DecimalField(db_column='TotalAmortizacion', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalinquilino = models.DecimalField(db_column='TotalInquilino', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalpensionista = models.DecimalField(db_column='TotalPensionista', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    deudaspendientes = models.NullBooleanField(db_column='Deudas')  # Field name made lowercase.
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
    observacionesadicionales = models.TextField(db_column='ObservacionesAdicionales',blank=True, null=True)  # Field name made lowercase.
    cod_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='Cod_colegio', blank=True, null=True)  # Field name made lowercase.
    cod_escuela = models.ForeignKey(Escuela, models.DO_NOTHING, db_column='Cod_Escuela', blank=True, null=True)  # Field name made lowercase.
    cod_user = models.ForeignKey( User,  models.DO_NOTHING, db_column='CodUser', blank=True, null=True)
    cod_seguros = models.ForeignKey( Seguros,  models.DO_NOTHING, db_column='CodSeguros', blank=True, null=True)
    cv = models.FileField(db_column='cv', upload_to=directorio_upload, null=True, blank=True)
    cvnombre = models.CharField(db_column='cvnombre', max_length=200, blank=True, null=True)
    empleado = models.NullBooleanField(db_column='Empleado')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Sol].[Solicitudes'
 
class Universidad(models.Model):
    cod_univesidad = models.IntegerField(db_column='Cod_univesidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sol].[Universidades'

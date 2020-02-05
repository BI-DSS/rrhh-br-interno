#-*-coding: utf-8-*-
from django.forms import ModelForm
from django.forms.widgets import *
from django import forms
from solicitud.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

ESTADO_CIVIL = (
	('','---------'),
	('S', 'Soltero(a)'),
	('C', 'Casado(a)'),
	('U', 'Union Libre'),
	('V', 'Viudo'),
	('D', 'Divorciado'),

)

LICENCIA = (
	('', '-------------'),
	(True, 'SI'),
	(False, 'NO'),
)

AUTOMOVIL = (
	('', '-------------'),
	(True, 'SI'),
	(False, 'NO'),
)

POLIZA = (
	('', '-------------'),
	(True, 'SI'),
	(False, 'NO'),
)

DEPORTE = (
	('', '-------------'),
	(True, 'SI'),
	(False, 'NO'),
)

DEPORTES = (
	('Futbol', 'Futbol'),
	('Baloncesto', 'Baloncesto'),
	('Volibol', 'Volibol'),
	('Béisbol', 'Béisbol'),
	('Atletismo', 'Atletismo'),
	('Natación', 'Natación'),
	('Ciclismo', 'Ciclismo'),
	('Rugby', 'Rugby'),
	('Karate', 'Karate'),
	('Taekwondo', 'Taekwondo'),
	('Judo', 'Judo'),
	('Kung Fu', 'Kung Fu'),
	('Boxeo', 'Boxeo'),
	('Tenis', 'Tenis'),
	('Tenis de mesa','Tenis de mesa'),
	('Otro', 'Otro'),
)

IDIOMA = (
	('', '-----------'),
	('Ingles', 'Ingles'),
	('Aleman', 'Alemán'),
	('Frances', 'Frances'),
	('Portugues', 'Portugues'),
	('Italiano', 'Italiano'),
	('Otro', 'Otro'),
)

DEPENDENCIA_TIPO = (
	('','---------'),
	('T', 'Totalmente'),
	('P', 'Parcialmente'),
)

VIVIENDA_TIPO = (
	('', '--------'),
	('F', 'Con su familia'),
	('P', 'Propietario'),
	('I', 'Inquilino'),
	('E', 'Pensionista'),
)

DESPIDO =(
	('0', '------------'),
	('Despido', 'Despido'),
	('Renuncia', 'Renuncia'),

)

CUENTA_TIPO = (
	('', '--------'),
	('M', 'Depósitos monetarios'),
	('A', 'Depósitos de ahorro'),
	('O', 'Otros'),
)

PARENTESCO = (
	(' ', '---------'),
	('C', 'Conyugue'),
	('H', 'Hijo'),
	('I', 'Hija'),
	('P', 'Padre'),
	('M', 'Madre'),
	('F', 'Familiar'),
	('O', 'Otros'),
)

Orga = (
	(' ', '---------'),
	('Club Deportivo Olimpia', 'Club Deportivo Olimpia'),
	('Fundacion Hondureña para el niño con cancer', 'Fundacion Hondureña para el niño con cancer'),
	('Hogar diamante', 'Hogar diamante'),
	('Arca de las esperanzas', 'Arca de las esperanzas'),
)

sexo = (
	('femenino', 'Femenino'),
	('masculino', 'Masculino'),
)

NIVEL_ESTUDIO = (
	('0', '----------'),
	('1', 'PRIMARIA'),
	('2', 'SECUNDARIA'),
	('3', 'PREGRADO'),
	('4', 'POSTGRADO'),
	('5', 'DOCTORADO'),
)

class SolicitudFrm(ModelForm):
	estadocivil = forms.ChoiceField(choices=ESTADO_CIVIL, required=False, initial="Seleccione su estado civil")
	direccion_domicilio = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' ,'placeholder' : 'bloque 15, casa #...'}))
	automovil = forms.ChoiceField(choices=AUTOMOVIL, required=False)
	licencia = forms.ChoiceField(choices=LICENCIA, required=False)
	polizaseguro = forms.ChoiceField(choices=POLIZA, required=False)
	deporte = forms.ChoiceField(choices=DEPORTE, required=False)
	tipodeporte = forms.ChoiceField(choices=DEPORTES)
	hermanos = forms.ChoiceField(choices=DEPORTE, required=False)
	casado = forms.ChoiceField(choices=DEPORTE, required=False)
	hijos = forms.ChoiceField(choices=DEPORTE, required=False)
	dependientes = forms.ChoiceField(choices=DEPORTE, required=False)
	tipovivienda = forms.ChoiceField(choices=VIVIENDA_TIPO, required=False)
	cuentasbancarias = forms.ChoiceField(choices=DEPORTE, required=False)
	deudaspendientes = forms.ChoiceField(choices=DEPORTE, required=False)
	parentesco = forms.ChoiceField(choices=PARENTESCO, required=False)
	sexo = forms.ChoiceField(choices=sexo, widget=RadioSelect, required= False)
	direcciondomicilio = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	observaciones_adicionales = forms.CharField( widget=forms.Textarea(attrs={'rows' : '4'}), required=False)
	organizacion = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	domiciliopadre = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	direccionlaboralpadre = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	domiciliomadre = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	direccionlaboralmadre = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	domicilioconyugue = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	direccionlaboralconyugue = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)
	class Meta:
		model = Solicitud
		fields = '__all__'
		exclude = []


class HermanoFrm(ModelForm):
	domicilio = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' }), required=False)


	class Meta:
		model = Hermano
		fields = '__all__'
		exclude = []
		


class HijoFrm(ModelForm):

	nombres = forms.CharField(label="nombres", required=False )

	class Meta:
		model = Hijo
		fields = '__all__'
		exclude = []


class DependienteFrm(ModelForm):
	tipodependencia = forms.ChoiceField(choices=DEPENDENCIA_TIPO, required=False)

	class Meta:
		model = Dependiente
		fields = '__all__'
		exclude = []


class HistoriallaboralFrm(ModelForm):

	motivoretiro = forms.ChoiceField(choices=DESPIDO, required=False)
	direccionempresa = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' ,'placeholder' : 'calle los alc....'}))
	fucionespuesto = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' , 'placeholder' : 'Tareas que realizaba'}))
	class Meta:
		model = Historiallaboral
		fields = '__all__'
		exclude = []

class HistorialacademicoFrm(ModelForm):
	nivel_estudios=forms.ChoiceField(choices=(NIVEL_ESTUDIO), widget=forms.Select(attrs={'id':'select_niveles'}))
	class Meta:
		model = Historialacademico
		fields = '__all__'
		exclude = []


class CursoFrm(ModelForm):
	direccioncentroestudio = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' , 'placeholder' : ''}))

	class Meta:
		model = Curso
		fields = '__all__'
		exclude = []

class ReferenciaFrm(ModelForm):
	direccion = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' , 'placeholder' : ''}))
	class Meta:
		model = Referencia
		fields = '__all__'
		exclude = []

class ReferenciaPersonalFrm(ModelForm):
	direccion_personal = forms.CharField( widget=forms.Textarea(attrs={'rows' : '3' , 'placeholder' : ''}))

	class Meta:
		model = Referenciaspersonal
		fields = '__all__'
		exclude = []


class OrganizacionFrm(ModelForm):

	nombre = forms.ChoiceField(choices=Orga, required=False)
	seleccionadas = forms.CharField(widget=forms.Textarea(attrs={'rows' : '4' , 'readonly' :'readonly'}))
	class Meta:
		model = Organizacion
		fields = '__all__'
		exclude = []


class CuentaFrm(ModelForm):
	tipo_cuenta = forms.ChoiceField(choices=CUENTA_TIPO, required=False)

	class Meta:
		model = Cuenta
		fields = '__all__'
		exclude = []


class IdiomaFrm(ModelForm):
	nombre= forms.ChoiceField(choices=IDIOMA, required=False, widget=Select(attrs={'id':'select_idioma'}))
	class Meta:
		model = Idioma
		fields = '__all__'
		exclude = []

HABILIDADES = (
	('00', '----------'),
	('01', 'DISEÑO GRÁFICO'),
	('02', 'PROGRAMACIÓN'),
	('03', 'OFFICE'),
	('04', 'SOPORTE TÉCNICO'),
	('05', 'REDES E INFRAESTRUCTURA'),
)

class HabilidadFrm(ModelForm):
	nombre_habilidad = forms.ChoiceField(choices=HABILIDADES, widget=Select(attrs={'id':'select_habilidades'}))
	class Meta:
		model = Habilidad
		fields = '__all__'
		exclude = []

# -*- coding: utf-8 -*-	
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required ,permission_required
from django.contrib.auth.hashers  import make_password
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from general.models import *
from solicitud.models import *
from administrador.models import *
from solicitud.forms import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth.hashers import check_password
import base64
import uuid, json, pyodbc, os
from PIL import Image
from django.db import connection
from django.conf import settings
from django.core.files.base import ContentFile
from io import StringIO
from solicitud.forms import *
from django.db.models import Q

def force_to_unicode(text):
	return text if isinstance(text, unicode) else text.decode('latin-1')

def cerrar_sesion(request):
	logout(request)
	return redirect('/')

@transaction.atomic 
def login(request):
	areas = Areas.objects.all()
	if request.POST:
		with transaction.atomic():
			try:
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						auth_login(request, user)
						perfil = Solicitud.objects.get(cod_user=user.id)
						if perfil.estado == 0:
							return redirect('registro_dos')
						else:
							
							if 'url' in request.session:
								return redirect(request.session['url'])
							else:
								return redirect('perfil')
					else:
						mensaje_error = 'error_activacion'
						return render(request, 'page-login.html', {'mensaje':mensaje_error})
				return render(request, 'page-login.html', {'error':'Usuario y/o contraseña incorrectos'})
			except Exception as e:
				raise
	ctx={
	'areas':areas
	}
	return render(request, 'page-login.html' , ctx)

@transaction.atomic
def registro(request):
	areas = Areas.objects.all()
	if request.method == 'POST':
		with transaction.atomic():
			try:
				usuario = request.POST.get('correo')
				if not User.objects.filter(username=usuario).exists():
					user = User()
					user.username = request.POST.get('correo')
					user.first_name = request.POST.get('nombre')
					user.last_name = request.POST.get('apellido')
					user.set_password(request.POST.get('password'))
					user.is_active = False
					user.save()

					perfil = Solicitud()
					perfil.cod_user = user
					perfil.nombres = request.POST.get('nombre')
					perfil.primerapellido = request.POST.get('apellido')
					perfil.correo = request.POST.get('correo')
					perfil.estado = 0
					perfil.vista = 1
					perfil.save()

					import smtplib
					from email.mime.multipart import MIMEMultipart
					from email.mime.text import MIMEText
 
					if settings.EN_SERVIDOR == True:
						from django.contrib.sites.shortcuts import get_current_site
						current_site = get_current_site(request)
						url = "http://"+str(current_site.domain)+"/activarusuario/" + str(user.id) + "/"
						contenido_html = '<div style="text-align: center;width: 100%;font-family: Arial;font-weight: 100;"><h2>RECLUTAMIENTO BANRURAL</h2><h3>Link de Activación</h3><h5 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Para poder activar su cuenta, haga click <a href="'+ url +'" > aquí </a></h5></div>'

						email_from = 'ReclutamientoRRHH@banrural.com.hn'
						email_to = request.POST.get('correo')
						msg = MIMEMultipart('alternative')
						msg['Subject'] = 'Activación de Cuenta'
						msg['From'] = email_from
						msg['To'] = email_to
						msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
						server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
						server.sendmail(email_from, email_to, msg.as_string())
						server.quit()
					else:
						url = "http://localhost:8000/activarusuario/" + str(user.id) + "/"
						contenido_html = '<div style="text-align: center;width: 100%;font-family: Arial;font-weight: 100;"><h2>RECLUTAMIENTO BANRURAL</h2><h3>Link de Activación</h3><h5 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Para poder activar su cuenta, haga click <a href="'+ url +'" > aquí </a></h5></div>'

						email_from = 'juan.hernandez@bi-dss.com'
						email_to = request.POST.get('correo')
						msg = MIMEMultipart('alternative')
						msg['Subject'] = 'Activación de Cuenta'
						msg['From'] = email_from
						msg['To'] = email_to

						msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))

						# Credentials (if needed)
						username = 'juan.hernandez@bi-dss.com'
						password = 'Calito199410'

						# The actual mail send

						#server = smtplib.SMTP('192.168.1.50:25')
						server = smtplib.SMTP('smtp.office365.com:587')
						server.starttls()
						server.login(username,password)
						#server.sendmail(fromaddr, toaddrs + toaddrs2 , msg.as_string())
						server.sendmail(email_from, email_to, msg.as_string())
						server.quit()
					return render(request, 'registro_viejo.html', {'mensaje':'activacion'})
				else:
					return render(request, 'registro_viejo.html', {'mensaje':'existe'})
			except Exception as e:
				raise e

	ctx={
	'areas':areas
	}
	return render(request, 'registro_viejo.html', ctx)


@login_required(login_url= "/promocion-interna/")
def cargar_municipios(request):
	if request.is_ajax():
		cod_departamento = request.GET['cod_departamento']
		data = list(Municipio.objects.values('codmunicipio', 'descripcionmunicipio').filter(coddepartamento=cod_departamento))
		return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def registro_dos(request):
	solicitud = Solicitud.objects.get(cod_user=request.user.id)
	if request.method == 'POST':
		with transaction.atomic():
			try:
				foto_usuario = request.FILES.get('foto_usuario')
				datos_imagen = request.POST.get('datos_imagen')
				#Cortar imagen
				if datos_imagen != '' and datos_imagen !=None:
					image =  Image.open(foto_usuario)
					ancho, alto = image.size
					size = (int(ancho), int(alto))
					nueva_imagen = image.resize(size)
					region = (int(datos_imagen.split(",")[0]), int(datos_imagen.split(",")[1]), int(datos_imagen.split(",")[2]), int(datos_imagen.split(",")[3]))
					foto_perfil = nueva_imagen.crop(region)
					ruta_foto = 'foto_perfil_' + str(request.user.id) + '.jpg'
					foto_perfil.save(os.path.join(settings.MEDIA_ROOT, 'foto_perfil_' + str(request.user.id) + '.jpg'))
					Solicitud.objects.filter(cod_user=request.user.id).update(
						foto_usuario=ruta_foto,
						nombres = request.POST['nombres'],
						primerapellido = request.POST['apellidos'],
						estado=1 )
					return redirect('perfil')
				else:
					Solicitud.objects.filter(cod_user=request.user.id).update(
						nombres = request.POST['nombres'],
						primerapellido = request.POST['apellidos'],
						estado=1 )
					return redirect('perfil')

			except Exception as e:
				return render(request, 'registro_dos.html', {'error':'error', 'mensaje':e , 'solicitud':solicitud})
	return render(request, 'registro_dos.html', {'solicitud':solicitud})

def activar_usuario(request, id):
	try:
		User.objects.filter(id=id).update(is_active=True, is_staff=False)
		mensaje_activacion = "exito"
		return render(request, 'page-login.html', {'mensaje':mensaje_activacion})
	except Exception as e:
		mensaje_error = 'error'
		return render(request, 'page-login.html', {'mensaje':mensaje_error})

@login_required(login_url= "/promocion-interna/")
def perfil(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	lista_experiencias = Historiallaboral.objects.filter(codsolicitud__cod_user__id=request.user.id)
	lista_estudios = Historialacademico.objects.filter(codsolicitud__cod_user__id=request.user.id)
	
	try:
		return render(request, 'perfil.html', {'perfil':perfil, 'lista_experiencias':lista_experiencias, 'lista_estudios':lista_estudios})
	except Exception as e:
		return render(request, 'perfil.html', {'perfil':perfil, 'error':'error'})

	return render(request, 'perfil.html', {'perfil':perfil})

@login_required(login_url= "/promocion-interna/")
def datos_generales(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	ctx={'perfil':perfil}
	try:
		solicitud = Solicitud.objects.get(cod_user=request.user.id)
		lista_organizaciones = Organizacion.objects.filter(cod_solicitud=perfil.codsolicitud)
		ctx['lista_organizaciones'] = lista_organizaciones
		ctx['solicitud'] = solicitud
		return render(request, 'datos_generales.html', ctx)
	except Exception as e:
		print e
	return render(request, 'datos_generales.html', ctx)

@login_required(login_url= "/promocion-interna/")
def informacion_familiar(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	hermano = Hermano.objects.filter(codsolicitud__cod_user__id=request.user.id)
	hijo = Hijo.objects.filter(codsolicitud__cod_user__id=request.user.id)
	depen = Dependiente.objects.filter(codsolicitud__cod_user__id=request.user.id)
	ctx={'perfil': perfil,
		'hermano': hermano,
		'hijo': hijo,
		'depen': depen,
		}
	return render(request, 'informacion_familiar.html', ctx)

@login_required(login_url= "/promocion-interna/")
def informacion_economica(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	lista_cuentas = Cuenta.objects.filter(cod_solicitud__cod_user__id=request.user.id)
	ctx={'perfil':perfil, 'lista_cuentas':lista_cuentas}
	return render(request, 'informacion_economica.html', ctx)

@login_required(login_url= "/promocion-interna/")
def informacion_laboral(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	laboral = Historiallaboral.objects.values().filter(codsolicitud__cod_user__id=request.user.id)
	ctx={
	'perfil':perfil,
	'laboral': laboral
	}
	return render(request, 'informacion_laboral.html', ctx)

@login_required(login_url= "/promocion-interna/")
def informacion_academica(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	lista_estudios = Historialacademico.objects.filter(codsolicitud__cod_user__id=request.user.id)
	lista_cursos = Curso.objects.filter(codsolicitud__cod_user__id=request.user.id)
	lista_idiomas = Idioma.objects.filter(cod_solicitud__cod_user__id=request.user.id)
	lista_habilidades = Habilidad.objects.filter(cod_solicitud__cod_user__id=request.user.id)
	lista_competencias = Competencia.objects.filter(cod_solicitud__cod_user__id=request.user.id)
	form_habilidad = HabilidadFrm()
	ctx={'lista_competencias':lista_competencias, 'form_habilidad':form_habilidad, 'perfil':perfil,  'lista_estudios':lista_estudios, 'lista_habilidades':lista_habilidades, 'lista_cursos':lista_cursos, 'lista_idiomas':lista_idiomas}
	return render(request, 'informacion_academica.html', ctx)


@login_required(login_url= "/promocion-interna/")
def referencias(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	personal = Referenciaspersonal.objects.values().filter(codsolicitud__cod_user__id=request.user.id)
	laboral = Referencia.objects.values().filter(codsolicitud__cod_user__id=request.user.id)
	ctx={
	'perfil':perfil,
	'personal':personal,
	'laboral':laboral
	}
	return render(request, 'referencias.html', ctx)

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_datosgenerales(request, codigo):
	lista_paises = Pais.objects.all()
	solicitud = Solicitud.objects.get(codsolicitud=codigo)
	form = SolicitudFrm(instance=solicitud)
	lista_departamentos = Departamento.objects.filter(codpais=1)
	lista_municipios = Municipio.objects.filter(coddepartamento__codpais__codpais=1)
	lista_organizaciones = Organizacion.objects.filter(cod_solicitud=solicitud.codsolicitud)
	lista_seguros = Seguros.objects.all()
	if request.method == 'POST':
		with transaction.atomic():
			try:
				coduser = Solicitud.objects.get(codsolicitud=codigo).cod_user
				user = User.objects.get(pk = coduser.pk )
				user.first_name = request.POST.get('nombres')
				user.last_name = request.POST.get('primerapellido')
				user.save()
			
				pais_nacionalidad = Pais.objects.get(codpais=request.POST.get('nacionalidad'))
				Solicitud.objects.filter(codsolicitud=codigo).update(
					nombres=request.POST.get('nombres'),
					primerapellido=request.POST.get('primerapellido'),
					sexo=request.POST.get('sexo'),
					estadocivil=request.POST.get('estadocivil'),
					apellidocasada=request.POST.get('apellidocasada'),
					coddepartamentodomicilio=Departamento.objects.get(coddepartamento=int(request.POST.get('coddepartamentodomicilio'))),
					codmunicipiodomicilio=Municipio.objects.get(codmunicipio=int(request.POST.get('codmunicipiodomicilio'))),
					direcciondomicilio=request.POST.get('direcciondomicilio'),
					telefonofijo=request.POST.get('telefonofijo'),
					celular=request.POST.get('celular'),
					codpaisnacimiento=pais_nacionalidad,
					lugarnacimiento=pais_nacionalidad.descripcionpais,
					fechanacimiento=request.POST.get('fechanacimiento'),
					edad=request.POST.get('edad'),
					profesion=request.POST.get('profesion'),
					identidad=request.POST.get('identidad'),
					codmunicipioidentidad=Municipio.objects.get(codmunicipio=int(request.POST.get('codmunicipioidentidad'))),
					automovil=request.POST.get('automovil'),
					licencia=request.POST.get('licencia'), 
					liviana=request.POST.get('liviana'),
					pesada=request.POST.get('pesada'),
					motocicleta=request.POST.get('motocicleta'),
					polizaseguro=request.POST.get('polizaseguro'),
					companiapoliza= '' if request.POST.get('compania') == '' else Seguros.objects.get(cod_seguros=request.POST.get('compania')).compania_seguros,
					deporte=request.POST.get('deporte'),
					tipodeporte=request.POST.get('tipodeporte'),
					fechadeporte=request.POST.get('fechadeporte'),
					numeroihss=request.POST.get('numeroihss'),
					rtn=request.POST.get('rtn'),
					numeropasaporte=request.POST.get('numeropasaporte'),
					cod_seguros = '' if request.POST.get('compania') == '' else Seguros.objects.get(cod_seguros=request.POST.get('compania')) )
				Organizacion.objects.filter(cod_solicitud=codigo).delete()
				organizaciones_lista = request.POST.get('input_registros')
				if  organizaciones_lista != '':
					organizaciones_temp = organizaciones_lista.split("_")
					for org_temp in organizaciones_temp:
						if org_temp != '':
							values_org = org_temp.split("/")
							Organizacion.objects.create(
								cod_grupo_organizacion=values_org[0],
								nombre=values_org[1],
								cod_solicitud=solicitud.codsolicitud)
				return redirect('datos_personales')
			except Exception as e:
				raise
	
	
	contexto = {'solicitud':solicitud,
			 'lista_departamentos':lista_departamentos,
			 'lista_municipios':lista_municipios,
			 'lista_organizaciones':lista_organizaciones ,
			 'form':form,
			 'lista_seguros':lista_seguros,
			 'lista_paises':lista_paises
			 }
	return render(request, 'editar_1.html', contexto)

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_cuenta(request, codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Cuenta.objects.filter(pk=codigo).update(
					tipo_cuenta=request.POST.get('tipocuenta'),
					cantidad=request.POST.get('cantidad').replace(',',''),
					institucion=request.POST.get('institucion'),
					numero_cuenta= str(request.POST.get('numero')) )
				return redirect('informacion_economica')	
			except Exception as e:
				raise e

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def nueva_cuenta(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Cuenta.objects.create(
					tipo_cuenta=request.POST.get('nuevo_tipocuenta'),
					cantidad=request.POST.get('nueva_cantidad'),
					institucion=request.POST.get('nueva_institucion'),
					numero_cuenta= '' if request.POST.get('nuevo_numero')== '' else request.POST.get('nuevo_numero'),
					cod_solicitud=Solicitud.objects.get(codsolicitud=solicitud))
				return redirect('informacion_economica')
			except Exception as e:
				raise

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_vivienda(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=solicitud).update(
					tipovivienda = request.POST.get('tipovivienda'),
					totalinquilino = None if request.POST.get('totalinquilino') == '' else float(request.POST.get('totalinquilino')),
					totalamortizacion = None if request.POST.get('totalamortizacion') == '' else float(request.POST.get('totalamortizacion')),
					totalpensionista = None if request.POST.get('totalpensionista') == '' else float(request.POST.get('totalpensionista')))
				return redirect('informacion_economica')
			except Exception as e:
				raise

@login_required(login_url= "/promocion-interna/")
def eliminar_cuenta(request, codigo):
	Cuenta.objects.filter(cod_cuenta=codigo).delete()
	return redirect('informacion_economica')

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_deuda(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=solicitud).update(
					deudaspendientes = request.POST.get('deudas'),
					nombreacreedor = '' if request.POST.get('nombreacreedor') == '' else request.POST.get('nombreacreedor'),
					montodeuda = 0.0 if request.POST.get('montodeuda') == '' else float(request.POST.get('montodeuda')),
					cuotamensual = 0.0 if request.POST.get('cuotamensual') == '' else float(request.POST.get('cuotamensual')))
				return redirect('informacion_economica')
				
			except Exception as e:
				raise

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_embargo(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=solicitud).update(
					embargado = request.POST.get('embargo'),
					nombrequienembargo = '' if request.POST.get('nombrequienembargo') == '' else request.POST.get('nombrequienembargo'),
					motivoembargo = '' if request.POST.get('motivoembargo') == '' else request.POST.get('motivoembargo'),
					montoembargo = 0.0 if request.POST.get('montoembargo') == '' else float(request.POST.get('montoembargo')))
				return redirect('informacion_economica')
			except Exception as e:
				raise

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_otrainformacion(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=solicitud).update(
					valoresefectivo = request.POST.get('efectivo'),

					montoefectivo = 0.0 if request.POST.get('montoefectivo') == '' or  request.POST.get('montoefectivo') == None  else request.POST.get('montoefectivo').replace(',',''),
					familiaresinstitucion = request.POST.get('familiar'),
					nombrefamiliar = '' if request.POST.get('nombrefamiliar') == '' else request.POST.get('nombrefamiliar'),
					parentesco = '' if request.POST.get('parentesco') == '' else request.POST.get('parentesco'),
					puestofamiliar = '' if request.POST.get('puestofamiliar') == '' else request.POST.get('puestofamiliar'),
					nombrequienrecomienda = '' if request.POST.get('nombrequienrecomienda') ==  '' else request.POST.get('nombrequienrecomienda'))
				return redirect('informacion_economica')
			except Exception as e:
				print 'error',e


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_aspiracionlaboral(request, solicitud):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=solicitud).update(
					trabajarcualquierlugar = request.POST.get('fuerapais'),
					sueldopretende = 0.0 if request.POST.get('sueldopretende') == '' else float(request.POST.get('sueldopretende')),
					puestoquesolicita = request.POST.get('puestoquesolicita'),
					fechainicio = '' if request.POST.get('fechainicio') == '' else request.POST.get('fechainicio'))
				return redirect('informacion_economica')
			except Exception as e:
				raise
	
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_hermanos(request, codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Hermano.objects.filter(codhermano=codigo).update(
					nombrecompleto = request.POST.get('nombrecompleto'),
					edad = request.POST.get('edad'),
					domicilio = request.POST.get('domicilio'),
					telefono = request.POST.get('telefono'),
					ocupacion = request.POST.get('ocupacion'))
				return redirect('informacion_familiar')
			except Exception as e:
				raise


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_hermanos(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				valor= Solicitud.objects.get(codsolicitud=codigo)
				Hermano.objects.create(
					nombrecompleto = request.POST.get('nombrecompleto'),
					codsolicitud = valor,
					edad = request.POST.get('edad'),
					domicilio = request.POST.get('domicilio'),
					telefono = request.POST.get('telefono'),
					ocupacion = request.POST.get('ocupacion'))
				return redirect('informacion_familiar')
			except Exception as e:
				raise



@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_hijo(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Hijo.objects.filter(codhijo=codigo).update(
					nombreshijo = request.POST.get('nombreshijo'),
					apellidoshijo = request.POST.get('apellidoshijo'),
					edadhijo = request.POST.get('edadhijo')
					)
				return redirect('informacion_familiar')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_hijo(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				valor= Solicitud.objects.get(codsolicitud=codigo)
				Hijo.objects.create(
					codsolicitud= valor,
					nombreshijo = request.POST.get('nombreshijo'),
					apellidoshijo = request.POST.get('apellidoshijo'),
					edadhijo = request.POST.get('edadhijo')
					)
				return redirect('informacion_familiar')
			
			except Exception as e:
				raise


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_dependiente(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				valor= Solicitud.objects.get(codsolicitud=codigo)
				Dependiente.objects.create(
					codsolicitud= valor,
					nombredependiente = request.POST.get('nombredependiente'),
					tipodependencia = request.POST.get('tipodependencia')
					)
				return redirect('informacion_familiar')
			except Exception as e:
				raise


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_dependiente(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Dependiente.objects.filter(coddependiente=codigo).update(
					nombredependiente = request.POST.get('nombredependiente'),
					tipodependencia = request.POST.get('tipodependencia')
					)
				return redirect('informacion_familiar')
		
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_padre(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=codigo).update(
					nombrespadre = request.POST.get('nombrespadre'),
					apellidospadre = request.POST.get('apellidospadre'),
					edadpadre = 0 if request.POST.get('edadpadre') == '' else request.POST.get('edadpadre'),
					domiciliopadre = request.POST.get('domiciliopadre'),
					telefonopadre= request.POST.get('telefonopadre'),
					celularpadre= request.POST.get('celularpadre'),
					profesionpadre = request.POST.get('profesionpadre'),
					direccionlaboralpadre = request.POST.get('direccionlaboralpadre')
					)
				return redirect('informacion_familiar')
			
			except Exception as e:
				raise
			

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_madre(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=codigo).update(
					nombresmadre = request.POST.get('nombresmadre'),
					apellidosmadre = request.POST.get('apellidosmadre'),
					edadmadre = 0 if request.POST.get('edadmadre') == '' else request.POST.get('edadmadre'),
					domiciliomadre = request.POST.get('domiciliomadre'),
					telefonomadre=  request.POST.get('telefonomadre') ,
					celularmadre= request.POST.get('celularmadre'),
					profesionmadre = request.POST.get('profesionmadre'),
					direccionlaboralmadre = request.POST.get('direccionlaboralmadre')
					)
				return redirect('informacion_familiar')
			except Exception as e:
				raise
	

@login_required(login_url= "/promocion-interna/")
@transaction.atomic 
def update_conyugue(request, codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Solicitud.objects.filter(codsolicitud=codigo).update(
					nombreconyugue = request.POST.get('nombreconyugue'),
					edadconyugue = 0 if request.POST.get('edadconyugue') == '' else request.POST.get('edadconyugue'),
					domicilioconyugue = request.POST.get('domicilioconyugue'),
					telefonoconyugue=  request.POST.get('telefonoconyugue') ,
					profesionconyugue = request.POST.get('profesionconyugue'),
					direccionlaboralconyugue = request.POST.get('direccionlaboralconyugue')
					)
				return redirect('informacion_familiar')
			except Exception as e:
				return redirect('informacion_familiar')		

@login_required(login_url= "/promocion-interna/")
def delete_hermano(request , codigo):
	Hermano.objects.filter(codhermano=codigo).delete()
	return redirect('informacion_familiar')

@login_required(login_url= "/promocion-interna/")
def delete_hijo(request , codigo):
	Hijo.objects.filter(codhijo=codigo).delete()
	return redirect('informacion_familiar')

@login_required(login_url= "/promocion-interna/")
def delete_dependiente(request , codigo):
	Dependiente.objects.filter(coddependiente=codigo).delete()
	return redirect('informacion_familiar')

############################################# UPDATE LABORAL ###################################
@login_required(login_url= "/promocion-interna/")
@transaction.atomic 
def update_laboral(request, codigo):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	histo = Historiallaboral.objects.get(codempresa = codigo)
	historial = HistoriallaboralFrm(instance=histo)
	if request.POST:
		with transaction.atomic():
			try:
				Historiallaboral.objects.filter(codempresa = codigo).update(
					nombreempresa = request.POST.get('nombreempresa'),
					fechaingreso= request.POST.get('fechaingreso'),
					fechaegreso= None if request.POST.get('fechaegreso') == '' else request.POST.get('fechaegreso'),
					direccionempresa = request.POST.get('direccionempresa'),
					nombrejefeinmediato = request.POST.get('nombrejefeinmediato'),
					motivoretiro = request.POST.get('motivoretiro'),
					puesto = request.POST.get('puesto')[:100], 
					fucionespuesto = request.POST.get('fucionespuesto')[:100],
					salariofinal = request.POST.get('salariofinal')
					)
				return redirect('informacion_laboral')
			except Exception as e:
				raise
	ctx={
	'perfil':perfil,
	'histo':histo,
	'historial': historial,
	}

	return render(request, 'Update-laboral.html', ctx)

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_laboral(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	historial = HistoriallaboralFrm()
	if request.POST:
		with transaction.atomic():
			try:
				Historiallaboral.objects.create(
					codsolicitud = Solicitud.objects.get(cod_user=request.user.id),
					nombreempresa = request.POST.get('nombreempresa'),
					fechaingreso= request.POST.get('fechaingreso'),
					fechaegreso= None if request.POST.get('fechaegreso') == '' else request.POST.get('fechaegreso'),
					direccionempresa = request.POST.get('direccionempresa'),
					nombrejefeinmediato = request.POST.get('nombrejefeinmediato'),
					motivoretiro = request.POST.get('motivoretiro'),
					puesto = request.POST.get('puesto'),
					fucionespuesto = request.POST.get('fucionespuesto'),
					salariofinal = request.POST.get('salariofinal')
					)
				return redirect('informacion_laboral')

			except Exception as e:
				raise
	
	ctx={
	'perfil':perfil,
	'historial': historial,
	}

	return render(request, 'Update-laboral.html', ctx)

@login_required(login_url= "/promocion-interna/")
def delete_laboral(request , codigo):
	Historiallaboral.objects.filter(codempresa=codigo).delete()
	return redirect('informacion_laboral')

#################################### Referencias Personales ##########################################
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_referencia_personal(request):
	if request.POST:
		with transaction.atomic():
			try:
				Referenciaspersonal.objects.create(
					codsolicitud = Solicitud.objects.get(cod_user=request.user.id),
					nombre_personal = request.POST.get('nombre_personal'),
					profesion_personal = request.POST.get('profesion_personal'),
					direccion_personal = request.POST.get('direccion_personal'),
					telefono_personal = request.POST.get('telefono_personal')
					)
				return redirect('referencias')

			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_referencia_personal(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
			
				Referenciaspersonal.objects.filter(codreferenciapersonal = codigo).update(
					nombre_personal = request.POST.get('nombre_personal'),
					profesion_personal = request.POST.get('profesion_personal'),
					direccion_personal = request.POST.get('direccion_personal'),
					telefono_personal = request.POST.get('telefono_personal')
					)
				return redirect('referencias')
			except Exception as e:
				raise
			

@login_required(login_url= "/promocion-interna/")
def delete_referencia_personal(request , codigo):
	Referenciaspersonal.objects.filter(codreferenciapersonal = codigo).delete()
	return redirect('referencias')


########################################## Referencias Laborales #########################################
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_referencia_laboral(request):
	if request.POST:
		with transaction.atomic():
			try:
				Referencia.objects.create(
					codsolicitud = Solicitud.objects.get(cod_user=request.user.id),
					nombrecompleto = request.POST.get('nombrecompleto'),
					profesion = request.POST.get('profesion'),
					direccion = request.POST.get('direccion'),
					telefono = request.POST.get('telefono')
					)
				return redirect('referencias')
			except Exception as e:
				raise
			

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_referencia_laboral(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
				Referencia.objects.filter(codreferencia = codigo).update(
					nombrecompleto = request.POST.get('nombrecompleto'),
					profesion = request.POST.get('profesion'),
					direccion = request.POST.get('direccion'),
					telefono = request.POST.get('telefono')
					)
				return redirect('referencias')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
def delete_referencia_laboral(request , codigo):
	Referencia.objects.filter(codreferencia = codigo).delete()
	return redirect('referencias')

@login_required(login_url= "/promocion-interna/")
def configuracion(request):
	
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	lista_departamentos = Departamento.objects.filter(codpais=1)
	contexto = {'perfil':perfil, 'lista_departamentos':lista_departamentos}
	return render(request, 'configuracion.html', contexto)


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_infoperfil(request):

	if request.POST:
		with transaction.atomic():
			try:
				User.objects.filter(id=request.user.id).update(
					first_name = request.POST.get('nombre'),
					last_name = request.POST.get('apellido'))
				Solicitud.objects.filter(cod_user=request.user.id).update(
					nombre_usuario = request.POST.get('nombre'),
					apellido_usuario = request.POST.get('apellido'),
					cod_departamento = request.POST.get('departamento'),
					cod_municipio = request.POST.get('municipio'),
					direccion_usuario = request.POST.get('direccion'),
					telefono_celular = request.POST.get('celular'),
					telefono_fijo = request.POST.get('telefono'))
				return redirect('configuracion')
			except Exception as e:
				raise
		

	

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def cambiar_clave(request):
	if request.POST:
		with transaction.atomic():
			try:
				perfil = Solicitud.objects.get(cod_user=request.user.id)
				clave_nueva = request.POST.get('clave_actual')
				if check_password(clave_nueva, request.user.password):
					user = User.objects.get(id=request.user.id)
					user.set_password(request.POST.get('clave_nueva'))
					user.save()
					return render(request, 'configuracion.html', {'perfil':perfil, 'message':'exito'})
				else:
					return render(request, 'configuracion.html', {'perfil':perfil, 'message':'error'})
			except Exception as e:
				raise
		
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_curso(request, codigo):
	if request.POST:
		with transaction.atomic():
			try:
			
				Curso.objects.filter(codcurso=codigo).update(
					temacurso=request.POST.get('temacurso'),
					duracion=request.POST.get('duracion'),
					titulo=request.POST.get('titulo'),
					nombrecentroestudio=request.POST.get('nombrecentroestudio'),
					direccioncentroestudio=request.POST.get('direccioncentroestudio'))
				return redirect('informacion_academica')
			except Exception as e:
				raise
		
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def nuevo_curso(request):
	if request.POST:
		with transaction.atomic():
			try:
			
				solicitud = Solicitud.objects.get(cod_user=request.user.id)
				Curso.objects.create(
					temacurso=request.POST.get('temacurso'),
					duracion=request.POST.get('duracion'),
					titulo=request.POST.get('titulo'),
					nombrecentroestudio=request.POST.get('nombrecentroestudio'),
					direccioncentroestudio=request.POST.get('direccioncentroestudio'),
					codsolicitud=solicitud)
				return redirect('informacion_academica')
			except Exception as e:
				raise
	
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def nuevo_estudio(request):
	formestudios = HistorialacademicoFrm()
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	niveles_de_estudio = {'1':'PRIMARIA','2':'SECUNDARIA','3':'PREGRADO','4':'POSTGRADO','5':'DOCTORADO'}
	if request.POST:
		with transaction.atomic():
			try:
			
				solicitud = Solicitud.objects.get(cod_user=request.user.id)
				nivel = request.POST.get('nivel_estudios')
				institucion_estudio = ''
				titulo_estudio = ''
				lugar_estudio = ''
				if nivel == '1':
					objeto_departamento = Departamento.objects.get(coddepartamento=int(request.POST.get('lugar_estudio')))
					institucion_estudio = request.POST.get('institucion_primaria_secundaria')
					lugar_estudio = objeto_departamento.descripciondepartamento
				elif nivel == '2':
					objeto_departamento = Departamento.objects.get(coddepartamento=int(request.POST.get('lugar_estudio')))
					lugar_estudio = objeto_departamento.descripciondepartamento
					institucion_estudio = request.POST.get('institucion_primaria_secundaria')
					titulo_estudio = request.POST.get('titulo_secundaria')
				else:
					objeto_universidad = Universidad.objects.get(cod_univesidad=int(request.POST.get('nombre_institucion')))
					objeto_titulo = Carrera.objects.get(cod_carreras=int(request.POST.get('titulo_universidad')))
					objeto_campus = Campus.objects.get(cod_campus=int(request.POST.get('lugar_estudio')))
					institucion_estudio = objeto_universidad.nombre
					lugar_estudio = objeto_campus.nombre
					titulo_estudio = objeto_titulo.nombre_carrera
				Historialacademico.objects.create(
					codsolicitud=solicitud,
					nombreinstitucion=institucion_estudio,
					nivelestudios=niveles_de_estudio[nivel],
					lugarestudio=lugar_estudio,
					tituloobtenido=titulo_estudio,
					inicio=int(request.POST.get('inicio')),
					fin=int(request.POST.get('fin')))
				return redirect('informacion_academica')
			except Exception as e:
				raise
		

	contexto = {'perfil':perfil, 'formestudios':formestudios }
	return render(request, 'nuevo_estudio.html', contexto)


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def editar_estudio(request, codigo):
	formestudios = HistorialacademicoFrm()
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	estudio = Historialacademico.objects.get(codinstitucion=codigo)
	niveles_de_estudio = {'1':'PRIMARIA','2':'SECUNDARIA','3':'PREGRADO','4':'POSTGRADO','5':'DOCTORADO'}
	if request.POST:
		with transaction.atomic():
			try:
			
				nivel = request.POST.get('nivel_estudios')
				institucion_estudio = ''
				titulo_estudio = ''
				lugar_estudio = ''
				if nivel == '1':
					objeto_departamento = Departamento.objects.get(coddepartamento=int(request.POST.get('lugar_estudio')))
					institucion_estudio = request.POST.get('institucion_primaria_secundaria')
					lugar_estudio = objeto_departamento.descripciondepartamento
				elif nivel == '2':
					objeto_departamento = Departamento.objects.get(coddepartamento=int(request.POST.get('lugar_estudio')))
					lugar_estudio = objeto_departamento.descripciondepartamento
					institucion_estudio = request.POST.get('institucion_primaria_secundaria')
					titulo_estudio = request.POST.get('titulo_secundaria')
				else:
					objeto_universidad = Universidad.objects.get(cod_univesidad=int(request.POST.get('nombre_institucion')))
					objeto_titulo = Carrera.objects.get(cod_carreras=int(request.POST.get('titulo_universidad')))
					objeto_campus = Campus.objects.get(cod_campus=int(request.POST.get('lugar_estudio')))
					institucion_estudio = objeto_universidad.nombre
					lugar_estudio = objeto_campus.nombre
					titulo_estudio = objeto_titulo.nombre_carrera
				Historialacademico.objects.filter(codinstitucion=codigo).update(
					nombreinstitucion=institucion_estudio,
					nivelestudios=niveles_de_estudio[nivel],
					lugarestudio=lugar_estudio,
					tituloobtenido=titulo_estudio,
					inicio=int(request.POST.get('inicio')),
					fin=int(request.POST.get('fin')))
				return redirect('informacion_academica')
			except Exception as e:
				raise
		
	contexto = {'perfil':perfil, 'formestudios':formestudios, 'estudio':estudio}
	return render(request, 'editar_estudio.html', contexto)

###################################### HABILIDADES #########################################
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_habilidades(request):
	if request.POST:
		with transaction.atomic():
			try:
				Habilidad.objects.create(
					cod_solicitud = Solicitud.objects.get(cod_user=request.user.id),
					nombre_habilidad = request.POST.get('nombre_habilidad'),
					porcentaje = request.POST.get('porcentaje_habilidad')
					)
				return redirect('informacion_academica')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_habilidades(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
			
				por = 'porcentaje_habilidad-' + str(codigo)
				porcentaje = request.POST.get(por)
				Habilidad.objects.filter(cod_habilidad = codigo).update(
					nombre_habilidad = request.POST.get('nombre_habilidad'),
					porcentaje = int(porcentaje)
					)
				return redirect('informacion_academica')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
def delete_habilidades(request , codigo):
	Habilidad.objects.filter(cod_habilidad = codigo).delete()
	return redirect('informacion_academica')

@login_required(login_url= "/promocion-interna/")
def eliminar_competencia(request, codigo):
	Competencia.objects.filter(cod_compentencias=codigo).delete()
	return redirect('informacion_academica')

COMPETENCIAS = {'1':'TRABAJO EN EQUIPO', '2':'PUNTUALIDAD', '3':'LIDERAZGO', '4':'INNOVACION', '5':'CREATIVIDAD', '6':'INICIATIVA'}

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def agregar_competencias(request):
	if request.POST:
		with transaction.atomic():
			try:
			
				solicitud = Solicitud.objects.get(cod_user=request.user.id)
				competencias = request.POST.get('competencias')
				if competencias != '':
					lista_competencias = competencias.split("/")
					for competencia in lista_competencias:
						if	competencia != '':
							Competencia.objects.create(
								nombre_competencia=COMPETENCIAS[competencia],
								posee=True,
								cod_solicitud=solicitud)
				return redirect('informacion_academica')
			except Exception as e:
				raise
		
@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def create_idioma(request):
	if request.POST:
		with transaction.atomic():
			try:
				Idioma.objects.create(
					cod_solicitud = Solicitud.objects.get(cod_user=request.user.id),
					nombre = request.POST.get('nombre_idioma'),
					habla = request.POST.get('expresion-nuevo-idioma'),
					escritura = request.POST.get('escritura-nuevo-idioma'),
					lectura = request.POST.get('lectura-nuevo-idioma')
					)
				return redirect('informacion_academica')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def update_idioma(request , codigo):
	if request.POST:
		with transaction.atomic():
			try:
			
				exp='expresion-editar-idioma-'+str(codigo)
				expresion=request.POST.get(exp)
				lec = 'lectura-editar-idioma-'+ str(codigo)
				lectura = request.POST.get(lec)
				esc = 'escritura-editar-idioma-'+str(codigo)
				escritura = request.POST.get(esc)
				Idioma.objects.filter(cod_idioma = codigo).update(

					nombre = request.POST.get('nombre_idioma-editar'),
					habla = expresion,
					escritura = escritura,
					lectura = lectura
					)
				return redirect('informacion_academica')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
def delete_idioma(request , codigo):
	Idioma.objects.filter(cod_idioma = codigo).delete()
	return redirect('informacion_academica')


@transaction.atomic
def recuperar_clave(request):
	if request.method == 'POST':
		with transaction.atomic():
			try:
			
				correo = request.POST.get('email_user')
				if User.objects.filter(username=correo).exists():
					#Generación de password tempral
					from random import choice
					longitud = 12
					valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
					nueva_clave = ""
					nueva_clave = nueva_clave.join([choice(valores) for i in range(longitud)])
					
					user = User.objects.get(username=correo)
					user.set_password(nueva_clave)
					user.save()
					#Envío de correo
					import smtplib
					from email.mime.multipart import MIMEMultipart
					from email.mime.text import MIMEText

					if settings.EN_SERVIDOR == True:
						from django.contrib.sites.shortcuts import get_current_site
						current_site = get_current_site(request)
						url = "http://"+str(current_site.domain)+"/login/"
						contenido_html = '<div style="text-align: center;width: 100%;font-family: Arial;font-weight: 100;"><h2>RECLUTAMIENTO BANRURAL</h2><h3>Recuperación de Contraseña</h3><h4 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Su contraseña temporal es la siguiente, favor ingrese y cambiela a la brevedad posible: <b>'+ nueva_clave +'</b></h4><h5 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Para ingresar y cambiar su clave, haga click <a target="_blank" href="'+ url +'" > aquí </a></h5></div>'

						email_from = 'ReclutamientoRRHH@banrural.com.hn'
						email_to = correo
						msg = MIMEMultipart('alternative')
						msg['Subject'] = 'Recuperación de Contraseña'
						msg['From'] = email_from
						msg['To'] = email_to

						msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))

						server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
						server.sendmail(email_from, email_to, msg.as_string())
						server.quit()
					else:
						url = "http://localhost:8000/login/"
						contenido_html = '<div style="text-align: center;width: 100%;font-family: Arial;font-weight: 100;"><h2>RECLUTAMIENTO BANRURAL</h2><h3>Recuperación de Contraseña</h3><h4 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Su contraseña temporal es la siguiente, favor ingrese y cambiela a la brevedad posible: <b>'+ nueva_clave +'</b></h4><h5 style="font-family: Arial;font-weight: 100;padding: 0 15% 0 15%;">Para ingresar y cambiar su clave, haga click <a target="_blank" href="'+ url +'" > aquí </a></h5></div>'

						email_from = '900007@banrural.com.hn'
						email_to = correo
						msg = MIMEMultipart('alternative')
						msg['Subject'] = 'Recuperación de Contraseña'
						msg['From'] = email_from
						msg['To'] = email_to

						msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))

						# Credentials (if needed)
						username = '900007@banrural.com.hn'
						password = 'Temporal32z'

						#server = smtplib.SMTP('192.168.1.50:25')
						server = smtplib.SMTP('smtp.office365.com:587')
						server.starttls()
						server.login(username,password)
						server.sendmail(email_from, email_to, msg.as_string())
						server.quit()
					return render(request, 'page-login.html', {'mensaje':'exito_clave'})
				else:
					return render(request, 'page-login.html', {'mensaje':'error_clave'})
			except Exception as e:
				raise e
	return render(request, 'page-login.html')


###################### ver ofertas ##################################

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]


def todas_ofertas(request):
	cursor = connection.cursor()
	try:
		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
		cursor.execute(query)
		areas = dictfetchall(cursor)
	except Exception as e:
		raise e
	finally:
		cursor.close()
	oferta = Ofertas.objects.filter(Estado= True , Publica= True ).order_by('-Fecha_publicacion')
	
	if request.POST:
		perfil = Solicitud.objects.get(cod_user=request.user.id)
		oferta = Ofertas.objects.filter(Estado = True, Publica= True).filter(Q(Puesto_oferta__contains=request.POST['filtrar']) | Q(Perfil_candidato__contains=request.POST['filtrar']) | Q(Municipio__contains=request.POST['filtrar']) | Q(Departamento__contains=request.POST['filtrar']) | Q(Tipo_contratacion__contains=request.POST['filtrar']) | Q(Descripcion_area__contains=request.POST['filtrar']) )
		cursor = connection.cursor()
		try:
			query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply ( select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area ) x"
			cursor.execute(query)
			areas = dictfetchall(cursor)
		except Exception as e:
			raise e
		finally:
			cursor.close()

		return render(request, 'blog.html', {'oferta':oferta, 'areas':areas ,'perfil':perfil})

	todas = True	
	return render(request, 'blog.html', {'oferta':oferta, 'areas':areas, 'todas':todas})

# def blog(request):
# 	oferta = Ofertas.objects.filter(Estado = True, Publica= True).filter(Estado= True , Publica= True).order_by('-Fecha_publicacion')[:10]
# 	cursor = connection.cursor()
# 	try:
# 		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
# 		cursor.execute(query)
# 		areas = dictfetchall(cursor)
# 	except Exception as e:
# 		raise e
# 	finally:
# 		cursor.close()

# 	if request.POST:
# 		oferta = Ofertas.objects.filter(Estado = True, Publica= True).filter(Q(Puesto_oferta__contains=request.POST['filtrar']) | Q(Perfil_candidato__contains=request.POST['filtrar']) | Q(Municipio__contains=request.POST['filtrar']) | Q(Departamento__contains=request.POST['filtrar']) | Q(Tipo_contratacion__contains=request.POST['filtrar']) | Q(Descripcion_area__contains=request.POST['filtrar']) )
# 		try:
# 			cursor = connection.cursor()
# 			query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
# 			cursor.execute(query)
# 			areas = dictfetchall(cursor)
# 		except Exception as e:
# 			raise e
# 		finally:
# 			cursor.close()

# 		return render(request, 'blog.html', {'oferta':oferta, 'areas':areas})

# 	return render(request, 'blog.html', {'oferta':oferta, 'areas':areas})


def blog(request):
	div = ''
	#User.objects.update(is_active = True)
	#print 'Pase por aqui'
	url =  str( request.build_absolute_uri() )
	if url != 'http://192.168.2.46:8000/':
		div = 'pagination'

	oferta = Ofertas.objects.filter(Estado = True, Publica= True).filter(Estado= True , Publica= True).order_by('-Fecha_publicacion')
	page = request.GET.get('page', 1)
	paginator = Paginator(oferta, 10)
	try:
		oferta = paginator.page(page)
	except PageNotAnInteger:
		oferta = paginator.page(1)
	except EmptyPage:
		oferta = paginator.page(paginator.num_pages)
	try:
		cursor = connection.cursor()
		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
		cursor.execute(query)
		areas = dictfetchall(cursor)
	except Exception as e:
		raise e
	finally:
		cursor.close()

	if request.POST:
		oferta = Ofertas.objects.filter(Estado = True, Publica= True).filter(Q(Puesto_oferta__contains=request.POST['filtrar']) | Q(Perfil_candidato__contains=request.POST['filtrar']) | Q(Municipio__contains=request.POST['filtrar']) | Q(Departamento__contains=request.POST['filtrar']) | Q(Tipo_contratacion__contains=request.POST['filtrar']) | Q(Descripcion_area__contains=request.POST['filtrar']) )
		try:
			cursor = connection.cursor()
			query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
			cursor.execute(query)
			areas = dictfetchall(cursor)
		except Exception as e:
			raise e
		finally:
			cursor.close()

		return render(request, 'blog-internas.html', {'oferta':oferta, 'areas':areas, 'div':div})

	return render(request, 'blog-internas.html', {'oferta':oferta, 'areas':areas, 'div':div})


@permission_required('empleado.ver_internas')
@login_required(login_url= "/promocion-interna/")
def blog_internas(request):
	oferta = Ofertas.objects.filter(Estado= True , Interna=True).order_by('-Fecha_publicacion')
	try:
		cursor = connection.cursor()
		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Interna='True' group by o.cod_area) x"
		cursor.execute(query)
		areas = dictfetchall(cursor)
	except Exception as e:
		raise e
	finally:
		cursor.close()

	if request.POST:
		oferta = Ofertas.objects.filter(Estado= True , Interna=True).filter(Q(Puesto_oferta__contains=request.POST['filtrar']) | Q(Perfil_candidato__contains=request.POST['filtrar']) | Q(Municipio__contains=request.POST['filtrar']) | Q(Departamento__contains=request.POST['filtrar']) | Q(Tipo_contratacion__contains=request.POST['filtrar']) | Q(Descripcion_area__contains=request.POST['filtrar']) )
		try:
			cursor = connection.cursor()
			query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Interna='True' group by o.cod_area) x"
			cursor.execute(query)
			areas = dictfetchall(cursor)
		except Exception as e:
			raise e
		finally:
			cursor.close()

		return render(request, 'blog-internas.html', {'oferta':oferta, 'areas':areas})

	return render(request, 'blog-internas.html', {'oferta':oferta, 'areas':areas})



def filtro_depto(request , codigo):
	area = Areas.objects.get(Cod_area= codigo)
	oferta = Ofertas.objects.filter(Cod_area= codigo, Estado= True , Publica= True)
	try:
		cursor = connection.cursor()
		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Publica='True' group by o.cod_area) x"
		cursor.execute(query)
		areas = dictfetchall(cursor)
	except Exception as e:
		areas = e
		pass
	finally:
		cursor.close()

	

	return render(request, 'blog-depto.html', {'oferta':oferta, 'areas':areas, 'area':area })

@transaction.atomic
def aplicar_oferta(request , codigo):
	request.session['url'] = "/aplicar-oferta/"+str(codigo)+"/"
	oferta = Ofertas.objects.get(Cod_oferta = codigo)
	Cod_area = oferta.Cod_area
	ofertas= Ofertas.objects.filter(Cod_area = Cod_area, Estado = True , Interna= True).exclude(Cod_oferta = codigo)[:5]
	pregunta = Preguntas.objects.filter(Cod_oferta = codigo)
	try:
		cursor = connection.cursor()
		query = "select Cod_area, Descripcion_area, COALESCE(Cantidad, 0) Cantidad from [Ofe].[Areas] a outer apply (select count(*) Cantidad from [Ofe].[Ofertas] o where a.[Cod_area] = o.cod_area and o.Estado= 'True' and o.Interna='True' group by o.cod_area) x"
		cursor.execute(query)
		areas = dictfetchall(cursor)
	except Exception as e:
		raise e 
	finally:
		cursor.close()

	mensaje = ""

	if request.POST:
		with transaction.atomic():
			try:
				solicitud = Solicitud.objects.get(cod_user=request.user.id)
				if Aplicaciones.objects.filter(Cod_solicitud=solicitud , Cod_oferta = codigo ).count() == 0 and solicitud.vista == 7:
					preguntas =Preguntas.objects.filter(Cod_oferta = codigo).values_list('Cod_pregunta', flat= True)
					soli = Solicitud.objects.get(cod_user=request.user.id)
					aplicacion = Aplicaciones()
					aplicacion.Cod_oferta = Ofertas.objects.get(Cod_oferta = codigo)
					aplicacion.Cod_solicitud = Solicitud.objects.get(cod_user=request.user.id)
					aplicacion.save()

					for x in preguntas:
						respuesta = Respuestas()
						pre = Preguntas.objects.get(Cod_pregunta = x)
						respuesta.Cod_pregunta = pre
						respuesta.Descripcion_pregunta = pre.Descripcion_pregunta
						respuesta.Cod_solicitud = soli
						respuesta.Cod_aplicacion = aplicacion
						respuesta.Cod_oferta = Ofertas.objects.get(Cod_oferta = codigo)
						y = str(x)
						respuesta.Descripcion_respuesta = request.POST.get(y)
						respuesta.save()
					mensaje = 1
				else:
					print 'No entreee'
					mensaje = 0
					
				return HttpResponseRedirect(reverse('mensaje_page', kwargs={'mensaje':mensaje}))

			except Exception as e:
				raise e
		

	return render(request , 'aplicar_ofertas.html', {'oferta':oferta , 'pregunta':pregunta , 'ofertas':ofertas , 'areas':areas})


def mensaje_page(request, mensaje ):
	if mensaje == '1':
		mens = "Éxito"
	else:
		mens = "Error"


	return render(request, 'pagina_respuestas.html', {'mens':mens})


@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def cambiar_cv(request):

	if request.POST:
		with transaction.atomic():
			try:				
				request.FILES['cv'].name = force_to_unicode(request.FILES['cv'].name)
				registro = Solicitud.objects.get(cod_user=request.user.id)
				archivo_path = 'media/'+registro.cv.path
				os.remove(registro.cv.path)
				registro.cv = request.FILES['cv']
				registro.cvnombre = request.FILES['cv'].name
				registro.save()

				return redirect('perfil')
			except Exception as e:
				raise
		

@login_required(login_url= "/promocion-interna/")
@transaction.atomic
def cambiar_imagen(request):
	perfil = Solicitud.objects.get(cod_user=request.user.id)
	if request.method == 'POST':
		with transaction.atomic():	
			try:
				foto_usuario = request.FILES.get('foto_usuario')
				datos_imagen = request.POST.get('datos_imagen')
				#Cortar imagen
				with transaction.atomic():
					try:
						image =  Image.open(foto_usuario)
						ancho, alto = image.size
						size = (int(ancho), int(alto))
						nueva_imagen = image.resize(size)
						region = (int(datos_imagen.split(",")[0]), int(datos_imagen.split(",")[1]), int(datos_imagen.split(",")[2]), int(datos_imagen.split(",")[3]))
						foto_perfil = nueva_imagen.crop(region)
						ruta_foto = 'foto_perfil_' + str(request.user.id) + '.jpg'
						foto_perfil.save(os.path.join(settings.MEDIA_ROOT, 'foto_perfil_' + str(request.user.id) + '.jpg'))
						Solicitud.objects.filter(cod_user=request.user.id).update(foto_usuario=ruta_foto)
						return redirect('configuracion')
					except Exception as e:
						return render(request, 'configuracion.html', {'error':'error', 'mensaje':e, 'perfil':perfil})
			except Exception as e:
				return render(request, 'configuracion.html', {'error':'error', 'mensaje':e, 'perfil':perfil})
		return redirect('configuracion')

@transaction.atomic
def suscribirse(request):

	if request.POST:
		arealista = request.POST.getlist('area[]')
		correo = request.POST.get('correo')
		with transaction.atomic():
			try:
				for x in arealista:
					if x != '' and x != None:
						if not Suscriptores.objects.filter(Correo = correo , Cod_area= x).exists():
							sus= Suscriptores()
							sus.Correo = correo
							sus.Cod_area = Areas.objects.get(Cod_area = x)
							sus.Estado = True
							sus.save()

				import mimetypes
				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText
				from email.MIMEBase import MIMEBase
				from email.Encoders import encode_base64

				if settings.EN_SERVIDOR == True:
					contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">¡Muchas Gracias!</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">A partir de este momento estas suscrito en nuestra plataforma de reclutamiento BANRURAL y cada vez que abramos una plaza de trabajo de tu interes seras de los primeros en saberlo. </p></div></div></div>'

					email_from = 'ReclutamientoRRHH@banrural.com.hn'
					email_to = correo
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'Suscripción'
					msg['From'] = email_from
					msg['To'] = email_to
					msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
					server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
					server.sendmail(email_from, email_to, msg.as_string())
					server.quit()
					return redirect('blog')
				else:
					contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">¡Muchas Gracias!</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">A partir de este momento estas suscrito en nuestra plataforma de reclutamiento BANRURAL y cada vez que abramos una plaza de trabajo de tu interes seras de los primeros en saberlo. </p></div></div></div>'

					email_from = '900007@banrural.com.hn'
					email_to = correo
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'Suscripción'
					msg['From'] = email_from
					msg['To'] = email_to
					msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
					# Credentials (if needed)
					username = '900007@banrural.com.hn'
					password = 'Temporal32z'

					# The actual mail send

					#server = smtplib.SMTP('192.168.1.50:25')
					server = smtplib.SMTP('smtp.office365.com:587')
					server.starttls()
					server.login(username,password)
					#server.sendmail(fromaddr, toaddrs + toaddrs2 , msg.as_string())
					server.sendmail(email_from, email_to, msg.as_string())
					server.quit()			

					return redirect('blog')
			except Exception as e:
				raise

		




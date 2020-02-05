# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from solicitud.models import *
from general.models import *
from administrador.models import *
from solicitud.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.auth.decorators import login_required,  permission_required
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User ,  Group
import ldap
import smtplib
import mimetypes
from email.Encoders import encode_base64
from django.http import *
from django.template import RequestContext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.views.generic import View
from RRHH.utils import render_to_pdf
from django.db import connection
from django.db import transaction, IntegrityError
import json , os
import datetime
from django.conf import settings
from django.utils.dateparse import parse_date
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils import translation
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
from django.utils import formats
from django.utils.encoding import smart_str , smart_unicode
import locale

locale.setlocale(locale.LC_ALL, '')
def force_to_unicode(text):
	return text if isinstance(text, unicode) else text.decode('latin-1')

# Create your views here.
def auth(username, password):
	conn = ldap.initialize('ldap://192.168.1.11:389')
	conn.protocol_version = 3
	conn.set_option(ldap.OPT_REFERRALS, 0)
	try:
		result = conn.simple_bind_s('GFBanruralHN\\'+username, password)
	except ldap.INVALID_CREDENTIALS:
		return "Invalid credentials"
	except ldap.SERVER_DOWN:
		return "Server down"
	except ldap.LDAPError, e:
		if type(e.message) == dict and e.message.has_key('desc'):
			return "Other LDAP error: " + e.message['desc']
		else:
			return "Other LDAP error: " + e
	finally:
		conn.unbind_s()
	return True

def busqueda_active(request, usuario):
	result_set = []
	if settings.EN_SERVIDOR==True:
		conn = ldap.initialize('ldap://192.168.1.11')
		conn.protocol_version = 3
		conn.set_option(ldap.OPT_REFERRALS, 0)
		result = conn.simple_bind_s('GFBanruralHN\900007', 'Temporal32z')
		base_dn = ' ou=Locations, dc=banrural, dc=com, dc=hn'
		r = [str("mail")]
		s = "sAMAccountName=%s"%str(usuario)

		try:
			busqueda = conn.search(base_dn, ldap.SCOPE_SUBTREE,  s, r)
			while 1:
				result_type, result_data = conn.result(busqueda, 0)

				if (result_data == []):
					break
				else:
					if result_type == ldap.RES_SEARCH_ENTRY:
						result_data = list(result_data)
						result_set = result_data
		except ldap.LDAPError, e:
			print e

		conn.unbind_s()

		return result_set


# data = busqueda_active(request, usuario=request.GET['usuario'])
	# 			print 'data que vineiebie', data
	# 			data = data[0][0].split(',')
	# 			data =data[0].split('CN=')
	# 			data = {'nombre' : force_to_unicode(data[1])  }

@permission_required('super.crear_usuarios')
@login_required(login_url= '/administrador/')
@transaction.atomic
def usuario_nuevo(request):
	mensaje = ''
	if request.is_ajax():
		try:
			data = busqueda_active(request, usuario=request.GET['usuario'])
			data = data[0][1].split(',')
			data =data[0].split('CN=')
			data = {'nombre' : force_to_unicode(data[1])  }
		except Exception as e:
			print 'error',e
			data = []


		return HttpResponse(json.dumps(data), content_type='application/json')

	if request.POST:   
		with transaction.atomic():
			try:
				username = request.POST['txtCod_AC']
				correo = request.POST['txtCorreo']
				try:
					User.objects.get(username=username)
					mensaje = 'error'
				except Exception as e:
					usuario = User()
					usuario.username = username
					usuario.set_password(username)
					usuario.email = correo
					usuario.is_superuser = False
					usuario.is_staff= False
					usuario.is_active = True
					usuario.save()

					g = Group.objects.get(id=1)
					g.user_set.add(usuario)

					g = Group.objects.get(id=2)
					g.user_set.add(usuario)

					perfil= Solicitud()
					perfil.correo = correo
					perfil.cod_user = usuario
					perfil.vista = 1
					perfil.estado = 1
					perfil.empleado =True
					perfil.save()
					mensaje = 'exito'

			except Exception as e:
				raise e
	ctx={'mensaje': mensaje  }
	return render(request, 'nuevo_usuarios.html', ctx)

def logout_admin(request):
	logout(request)
	return redirect('login_admin')

@transaction.atomic
def login_admin(request):
	ctx = {}
	logout(request)
	if request.POST:
		with transaction.atomic():
			try:
				username = request.POST['username']
				password = request.POST['password']
				if settings.EN_SERVIDOR==True:
					active_directory = auth(username, password)
					if active_directory == True:
						try:
							user = User.objects.get(username = username)
							user.set_password(password)
							user.save()
							
						except Exception as e:
							pass
						usuario = authenticate(username=username, password=password)
						if usuario is not None:
							if usuario.has_perm('admin.ver_admin'):
								if User.objects.get(username = username).last_login != None:
									auth_login(request, user)
									return redirect('lista_candidatos')
					else:
						error = 'Credenciales no validas'
						ctx = {'error': error,'username': username}
						return render(request, 'login_admin.html', ctx)
				else:
					user = authenticate(username=username, password=password)
					if user is not None:
						if user.has_perm('admin.ver_admin'):
							auth_login(request, user)
							return redirect('lista_candidatos')
						else:
							ctx = {'error': True,'username': username}
							return render(request, 'login_admin.html', ctx)
					else:
						ctx = {'error': True,'username': username}
						return render(request, 'login_admin.html', ctx)
			except Exception as e:
				raise

	return render(request, 'login_admin.html') 

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def lista_candidatos(request):
	'''
	if not request.user.is_authenticated():
		return redirect('login_admin')
	else:
	'''
	import datetime
	fecha = datetime.date.today()
	candidatos = Aplicaciones.objects.filter(Fecha = fecha).count()
	ofertas = Ofertas.objects.all().count()
	ofertasA = Ofertas.objects.filter(Estado = True).count()
	ofertasD = Ofertas.objects.filter(Estado = False).count()
	registrados = User.objects.filter(is_active = True).exclude(groups__name__in=['Administrador']).count()

	cc = SeguimientoXAplicacion.objects.filter(CC = True).count()
	ctx = {
		'candidatos':candidatos,
		'ofertas':ofertas,
		'ofertasA':ofertasA,
		'ofertasD':ofertasD,
		'registrados':registrados,
		'cc':cc
		}
	return render(request, 'lista_candidatos.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def lista_registrados(request):
	lista =Solicitud.objects.filter(cod_user__is_active = 1).exclude(cod_user__groups__name='Administrador')
	total = User.objects.all().count()
	cantidad = lista.count()
	ctx = {
		'lista':lista,
		'cantidad':cantidad
		}
	return render(request, 'lista_registrados.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def perfil_candidato(request, solicitud):

	solicitud_candidato = Solicitud.objects.get(codsolicitud=solicitud)
	lista_experiencias = Historiallaboral.objects.filter(codsolicitud=solicitud)
	lista_estudios = Historialacademico.objects.filter(codsolicitud=solicitud)
	return render(request, 'candidato_perfil.html', {'solicitud':solicitud_candidato, 'lista_experiencias':lista_experiencias, 'lista_estudios':lista_estudios})


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def informacion_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	ctx={'solicitud':solicitud}
	try:
		lista_organizaciones = Organizacion.objects.filter(cod_solicitud=solicitud)
		ctx['lista_organizaciones'] = lista_organizaciones
		return render(request, 'candidato_informacion.html', ctx)
	except Exception as e:
		print e
	return render(request, 'candidato_informacion.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def familia_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	hermano = Hermano.objects.filter(codsolicitud=solicitud)
	hijo = Hijo.objects.filter(codsolicitud=solicitud)
	depen = Dependiente.objects.filter(codsolicitud=solicitud)
	ctx={'solicitud':solicitud,
		'hermano': hermano,
		'hijo': hijo,
		'depen': depen,
		}
	return render(request, 'candidato_familia.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def economia_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	lista_cuentas = Cuenta.objects.filter(cod_solicitud=solicitud)
	ctx={'solicitud':solicitud, 'lista_cuentas':lista_cuentas}
	return render(request, 'candidato_economia.html', ctx)


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def trabajo_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	laboral = Historiallaboral.objects.values().filter(codsolicitud=solicitud)
	ctx={'laboral': laboral, 'solicitud':solicitud}
	return render(request, 'candidato_trabajos.html', ctx)


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def estudios_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	lista_estudios = Historialacademico.objects.filter(codsolicitud=solicitud)
	lista_cursos = Curso.objects.filter(codsolicitud=solicitud)
	lista_idiomas = Idioma.objects.filter(cod_solicitud=solicitud)
	lista_habilidades = Habilidad.objects.filter(cod_solicitud=solicitud)
	lista_competencias = Competencia.objects.filter(cod_solicitud=solicitud)
	form_habilidad = HabilidadFrm()
	ctx={'lista_competencias':lista_competencias, 'form_habilidad':form_habilidad,'solicitud':solicitud, 'lista_estudios':lista_estudios, 'lista_habilidades':lista_habilidades, 'lista_cursos':lista_cursos, 'lista_idiomas':lista_idiomas}
	return render(request, 'candidato_estudios.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def referencias_candidato(request, solicitud):
	solicitud = Solicitud.objects.get(codsolicitud=solicitud)
	personal = Referenciaspersonal.objects.values().filter(codsolicitud=solicitud)
	laboral = Referencia.objects.values().filter(codsolicitud=solicitud)
	ctx={'personal':personal,'laboral':laboral, 'solicitud':solicitud}
	return render(request, 'candidato_referencia.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('super.crear_usuarios')
def lista_usuarios(request):
	lista_users = User.objects.filter(groups__name__in= ['administrador'])
	ctx  = {'lista_users':lista_users}
	return render(request, 'lista_usuarios.html', ctx)

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

############################## USUARIOS ADMINISTRADORES ######################

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def inhabilitar_usuario(request, codigo):

	User.objects.filter(username=codigo).update(
		is_active = False
		)
	return redirect('lista_usuarios')

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def habilitar_usuario(request, codigo):

	User.objects.filter(username=codigo).update(
		is_active = True
		)
	return redirect('lista_usuarios')

##############################OFERTAS LABORALES ############################
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def lista_ofertas(request):
	lista_publicas = Ofertas.objects.filter(Publica = True, Estado=True).order_by('-Fecha_publicacion')
	lista_internas = Ofertas.objects.filter(Interna = True , Estado=True).order_by('-Fecha_publicacion')
	lista_anonimas = Ofertas.objects.filter(Anonima = True , Estado=True).order_by('-Fecha_publicacion')
	# page = request.GET.get('page', 1)
	# paginator = Paginator(lista_publicas, 10)
	# try:
	# 	lista_publicas = paginator.page(page)
	# except PageNotAnInteger:
	# 	lista_publicas = paginator.page(1)
	# except EmptyPage:
	# 	lista_publicas = paginator.page(paginator.num_pages)

	# page = request.GET.get('page', 1)
	# paginator = Paginator(lista_internas, 10)
	# try:
	# 	lista_internas = paginator.page(page)
	# except PageNotAnInteger:
	# 	lista_internas = paginator.page(1)
	# except EmptyPage:
	# 	lista_internas = paginator.page(paginator.num_pages)

	# page = request.GET.get('page', 1)
	# paginator = Paginator(lista_anonimas, 10)
	# try:
	# 	lista_anonimas = paginator.page(page)
	# except PageNotAnInteger:
	# 	lista_anonimas = paginator.page(1)
	# except EmptyPage:
	# 	lista_anonimas = paginator.page(paginator.num_pages)

	return render(request, 'lista_ofertas.html',{'lista_publicas':lista_publicas , 'lista_internas':lista_internas,'lista_anonimas':lista_anonimas })

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic    
def oferta_nueva(request):
	import datetime
	lista_departamentos = Departamento.objects.filter(codpais=1)
	area = Areas.objects.all()
	if request.is_ajax():
		coddepartamento = request.GET['coddepartamento']
		data = list(Municipio.objects.values('codmunicipio', 'descripcionmunicipio').filter(coddepartamento = coddepartamento))
		return HttpResponse(json.dumps(data), content_type='application/json')
 
	if request.POST:
		with transaction.atomic():
			#try:
			preguntas = request.POST.getlist('preguntas[]')
			depto = Departamento.objects.get(pk=request.POST.get('Departamento'))
			mun = Municipio.objects.get(pk=request.POST.get('Municipio'))
			are = Areas.objects.get(pk=request.POST.get('area'))
			oferta = Ofertas()
			oferta.Puesto_oferta = request.POST.get('Puesto_oferta') 

			oferta.Descripcion_oferta = request.POST.get('Descripcion_oferta')
			oferta.Perfil_candidato = request.POST.get('Perfil_candidato')
			oferta.Fecha_publicacion = datetime.date.today()
			oferta.Cod_departamento = depto
			oferta.Departamento = depto.descripciondepartamento
			oferta.Cod_municipio = mun
			oferta.Municipio = mun.descripcionmunicipio 
			oferta.Estado = True
			oferta.Trabajo_campo = request.POST.get('Trabajo_campo')
			oferta.Vehiculo = request.POST.get('Vehiculo')
			oferta.Tipo_contratacion = request.POST.get('Tipo_contratacion')
			oferta.Edad_minima = request.POST.get('Edad_minima')
			oferta.Edad_maxima = request.POST.get('Edad_maxima')
			oferta.Disponibilidad = request.POST.get('Disponibilidad')
			oferta.Experiencia_laboral = request.POST.get('Experiencia_laboral')
			oferta.Cod_area = are
			oferta.Descripcion_area = are.Descripcion_area
			oferta.Publica = request.POST.get('publica')
			oferta.Interna = request.POST.get('interna')
			oferta.Anonima = request.POST.get('anonima')
			oferta.save()


			if preguntas != '' and preguntas != None and preguntas != []:
				counter = 0
				for x in preguntas:
					Preguntas.objects.create(
						Cod_oferta = oferta,
						Descripcion_pregunta = preguntas[counter])
					counter =+ 1

			email_to = Suscriptores.objects.values_list('Correo', flat=True).filter(Cod_area = are)

			NombrePlaza = oferta.Puesto_oferta
			NombreArea = oferta.Descripcion_area
			FechaCierre = oferta.Fecha_publicacion
			CodigoOfe = oferta.Cod_oferta
			if settings.EN_SERVIDOR == True:
				url = 'http://192.168.2.46:8003/vacantes/form_soli_1/'+str(CodigoOfe)
			else:
				url = 'http://localhost:8000/vacantes/form_soli_1/'+str(CodigoOfe)
			oferta = Ofertas.objects.filter(Cod_oferta = CodigoOfe).update(
				Url=url
				)
			if request.POST.get("publica") == True:
				import mimetypes
				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText
				from email.MIMEBase import MIMEBase
				from email.Encoders import encode_base64

				if settings.EN_SERVIDOR == True:
					contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">¡Nueva Oferta de Trabajo!</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">Se ha abierto una nueva plaza de : <b>'+NombrePlaza+'.</b> </p><p style="color: #201d33;  font-size: 18px;">En el area de : <b>'+NombreArea+'</b></p><p style="color: #201d33;  font-size: 18px;">Fecha Inicio: <b>'+FechaCierre+'</b></p><p style="color: #201d33;  font-size: 18px;">No pierdas esta gran oportunidad. <a href="http://192.168.1.221:8003/" target="_blank">Ir a Reclutamiento Banrural</a> para aplicar.</p><br></div></div></div>'

					email_from = 'ReclutamientoRRHH@banrural.com.hn'
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'Nueva Oferta de Trabajo'
					msg['From'] = email_from
					#msg['To'] = ', '.join(email_to)
					msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
					server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
					server.sendmail(email_from, email_to, msg.as_string())
					server.quit()
				else:
					contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">¡Nueva Oferta de Trabajo!</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">Se ha abierto una nueva plaza de : <b>'+NombrePlaza+'.</b> </p><p style="color: #201d33;  font-size: 18px;">En el area de : <b>'+NombreArea+'</b></p><p style="color: #201d33;  font-size: 18px;">Fecha Inicio: <b>'+FechaCierre+'</b></p><p style="color: #201d33;  font-size: 18px;">No pierdas esta gran oportunidad. <a href="http://localhost:8000/ " target="_blank">Ir a Reclutamiento Banrural</a> para aplicar.</p><br></div></div></div>'

					email_from = '900007@banrural.com.hn'
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'Nueva Oferta de Trabajo'
					msg['From'] = email_from
					#msg['To'] = ', '.join(email_to)
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
			#except Exception as e:
				#raise


	ctx = {'lista_departamentos': lista_departamentos , 'area':area}
	return render(request, 'oferta_nueva.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def update_oferta(request , codigo):
	import datetime
	ofer = Ofertas.objects.get(Cod_oferta = codigo)
	area = Areas.objects.all()
	pregun = Preguntas.objects.filter(Cod_oferta = codigo)
	pregunt = Preguntas.objects.values_list('Cod_pregunta', flat=True).filter(Cod_oferta = codigo)

	x = Respuestas.objects.filter(Cod_pregunta__in = pregunt).count()

	if x > 0:
		res = 1
	else:
		res = 0


	lista_departamentos = Departamento.objects.filter(codpais=1)
	
	if request.is_ajax():
		coddepartamento = request.GET['depto']
		data = list(Municipio.objects.values('codmunicipio', 'descripcionmunicipio').filter(coddepartamento = coddepartamento))
		return HttpResponse(json.dumps(data), content_type='application/json')
	if request.POST:
		with transaction.atomic():
			try:
				preguntas = request.POST.getlist('preguntas[]')
				depto = Departamento.objects.get(pk=request.POST.get('Departamento'))
				mun = Municipio.objects.get(pk=request.POST.get('Municipio'))
				Ofertas.objects.filter(Cod_oferta = codigo).update(
					Puesto_oferta = request.POST.get('Puesto_oferta'), 
					Descripcion_oferta = request.POST.get('Descripcion_oferta'),
					Perfil_candidato = request.POST.get('Perfil_candidato'),
					Cod_departamento = depto,
					Cod_municipio = mun,
					Departamento = depto.descripciondepartamento,
					Municipio = mun.descripcionmunicipio ,
					Estado = True,
					Trabajo_campo = request.POST.get('Trabajo_campo'),
					Vehiculo = request.POST.get('Vehiculo'),
					Tipo_contratacion = request.POST.get('Tipo_contratacion'),
					Edad_minima = request.POST.get('Edad_minima'),
					Edad_maxima = request.POST.get('Edad_maxima'),
					Disponibilidad = request.POST.get('Disponibilidad'),
					Experiencia_laboral = request.POST.get('Experiencia_laboral'),
					Publica = request.POST.get('publica'),
					Interna = request.POST.get('interna'),
					Anonima = request.POST.get('anonima'))
				
				if not x > 0:
					Preguntas.objects.filter(Cod_oferta = codigo).delete()
					oferta = Ofertas.objects.get(Cod_oferta = codigo)
					if preguntas != '':
						counter = 0
						for x in preguntas:
							Preguntas.objects.create(
								Cod_oferta = oferta,
								Descripcion_pregunta = preguntas[counter])
							counter =+ 1

				return redirect('lista_ofertas')
			except Exception as e:
				raise


	ctx = {'lista_departamentos': lista_departamentos, 'ofer':ofer , 'pregun':pregun ,'res':res , 'area':area}
	return render(request, 'update_plaza.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def inhabilitar_oferta(request, codigo):
	Ofertas.objects.filter(Cod_oferta =codigo).update(
		Estado= False
		)
	return redirect('lista_ofertas')

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def habilitar_oferta(request, codigo):
	Ofertas.objects.filter(Cod_oferta =codigo).update(
		Estado= True
		)
	return redirect('lista_ofertas')


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def solicitud_admin(request):
	if request.POST:
		with transaction.atomic():
			try:
				solicitud = Solicitud()
				solicitud.nombres = request.POST.get('nombres')
				solicitud.primerapellido = request.POST.get('apellidos')
				solicitud.profesion = request.POST.get('profesion')
				solicitud.celular = request.POST.get('telefono')
				solicitud.correo = request.POST.get('correo')
				solicitud.save()
				
				codigo = request.POST.get('codigo') 

				aplicacion = Aplicaciones()
				aplicacion.Cod_oferta = Ofertas.objects.get(Cod_oferta = codigo)
				aplicacion.Cod_solicitud = solicitud
				aplicacion.save()

				return redirect('lista_ofertas')
			except Exception as e:
				raise


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def candidatos_plaza(request, codigo):
	request.session['visto'] = '' 
	aplicaciones = Aplicaciones.objects.filter(Cod_oferta=codigo).order_by('-Fecha','Dislike')
	oferta = Ofertas.objects.get(Cod_oferta = codigo)
	ctx ={'aplicaciones':aplicaciones,  'oferta': oferta}
	return render(request , 'listaCan_plaza.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def favorito(request):
	if request.is_ajax():
		codigo = request.GET['codigo']
		with transaction.atomic():
			try:
				aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
				aplicacion.Favorito = True
				aplicacion.save()
				data = True
				return HttpResponse(json.dumps(data), content_type='application/json')
			except Exception as e:
				data = False
				return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def dislike(request , codigo):

	with transaction.atomic():
		try:
			aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
			aplicacion.Favorito = False
			aplicacion.save() 
			return redirect(reverse('lista_favoritos', kwargs={'codigo': aplicacion.Cod_oferta.Cod_oferta}))
		except Exception as e:
			raise


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def respuestas(request):

	if request.is_ajax():
		codigo_solicitud = request.GET['codigo_solicitud']
		codigo_oferta = request.GET['codigo_oferta']
		try:
			data = list(Respuestas.objects.values().filter(Cod_oferta = codigo_oferta, Cod_solicitud= codigo_solicitud ))
		except Exception as e:
			raise e
			data = {}
		
		return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def lista_favoritos(request , codigo):
	aplicaciones = Aplicaciones.objects.filter(Cod_oferta = codigo , Favorito= True)
	oferta = Ofertas.objects.get(Cod_oferta = codigo)
	ctx ={'aplicaciones':aplicaciones, 'oferta':oferta }

	return render(request, 'lista_favoritos.html', ctx)


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def seguimiento(request, codigo):
	aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
	lista_seguimiento = TipoSeguimiento.objects.all()

	if SeguimientoXAplicacion.objects.filter(Cod_Aplicacion = codigo).exists():
		seguimiento = SeguimientoXAplicacion.objects.filter(Cod_Aplicacion = codigo)[:1].get()
		ctx ={'aplicacion':aplicacion , 'lista_seguimiento':lista_seguimiento , 'seguimiento':seguimiento}
	else:
		ctx ={'aplicacion':aplicacion , 'lista_seguimiento':lista_seguimiento}

	return render(request, 'seguimiento.html', ctx)

#1
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Primera_entrevista(request , codigo):

	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		telefonoAnalista = request.POST['txtTelefono']
		extensionAnalista =  request.POST['txtExtension']
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)

		with transaction.atomic():
			try: 
				seguimiento = SeguimientoXAplicacion()
				seguimiento.Cod_Aplicacion = aplicacion
				seguimiento.Cod_Oferta = Ofertas.objects.get(Cod_oferta = aplicacion.Cod_oferta.pk)
				seguimiento.Cod_Solicitud = solicitud
				seguimiento.Pr_Entrevista = True
				seguimiento.Fch_Pr_Entrevista = request.POST.get('Fecha_Primera_entrevista')
				#Se construye la fecha y hora dependiendo de los datos seleccionados
				if request.POST.get('Tiempo') == 'pm':
					fecha_hora = "%s %s:%s:00" % (request.POST.get('Fecha_Primera_entrevista'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
				else:
					fecha_hora = "%s %s:%s:00" % (request.POST.get('Fecha_Primera_entrevista'), request.POST.get('hora'), request.POST.get('minuto') )
				seguimiento.Hor_Pr_Entrevista = fecha_hora
				seguimiento.save()
				#lugar = smart_unicode(request.POST['direccion'])
				lugar = " "
				# lugar= lugar.encode('latin-1').strip()
				# print "sjdndjiacnijsdncijsdncisdncijsdncisdn",lugar
				fecha = request.POST['Fecha_Primera_entrevista']
				values_fecha = fecha.split("-")
				year= values_fecha[0]
				month= values_fecha[1]
				day= values_fecha[2]

				if request.POST.get('Tiempo') == 'pm':
					hora = (int(request.POST.get('hora')) + 12)
				else:
					hora = request.POST.get('hora')
				minuto = request.POST.get('minuto')

				from datetime import datetime
				dt= datetime(int(year), int(month), int(day), int(hora), int(minuto), 50)
				fechita= dt.strftime("%d/%m/%Y %I:%M %p")
				miFecha = str(fechita)
				#CORREO DE LA CITA
				import smtplib
				from email.MIMEMultipart import MIMEMultipart
				from email.MIMEBase import MIMEBase
				from email.MIMEText import MIMEText
				from email.Utils import COMMASPACE, formatdate
				from email import Encoders
				import os,datetime

				if settings.EN_SERVIDOR == True:
					CRLF = "\r\n"
					correouser = correoAnalista
					attendees =[correo,correouser]
					organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
					fro = "BANRURAL <citas_reclutamiento@banrural.com.hn>"

					ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

					#ddtstart = datetime.datetime.now()
					dtoff = datetime.timedelta(days = 1)
					dur = datetime.timedelta(hours = 1)
					ddtstart = ddtstart + dtoff
					ddtstart = ddtstart + datetime.timedelta(hours = 6)
					dtend = ddtstart + dur
					dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
					dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
					dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

					description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
					attendee = ""
					for att in attendees:
					   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
					ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
					ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
					ical+= "UID:FIXMEUID"+dtstamp+CRLF
					ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
					ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
					nombre = solicitud.nombres +" "+solicitud.primerapellido
					eml_body = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>, a la dirección:  <b>'+ request.POST['direccion'] +'</b>. Fecha y Hora: <b>'+ miFecha +'</b></p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p><p style="color: red;">**Este correo es generico, no lo conteste**</p><br></div></div></div>'
					eml_body_bin = "This is the email body in binary - two steps"
					msg = MIMEMultipart('mixed')
					msg['Reply-To']=fro
					msg['Date'] = formatdate(localtime=True)
					msg['Subject'] = "Primera entrevista"
					msg['From'] = fro
					msg['To'] = ",".join(attendees)

					part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
					part_cal = MIMEText(ical,'calendar;method=REQUEST')

					msgAlternative = MIMEMultipart('alternative')
					msg.attach(msgAlternative)

					ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
					ical_atch.set_payload(ical)
					Encoders.encode_base64(ical_atch)
					ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

					eml_atch = MIMEBase('text/plain','')
					Encoders.encode_base64(eml_atch)
					eml_atch.add_header('Content-Transfer-Encoding', "")

					msgAlternative.attach(part_email)
					msgAlternative.attach(part_cal)


					mailServer = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
					mailServer.ehlo()
					mailServer.sendmail(fro, attendees, msg.as_string())
					mailServer.close()
					return redirect(reverse('seguimiento', kwargs={'codigo': aplicacion.Cod_aplicacion}))

				else:
					CRLF = "\r\n"
					login = "juancalihernandez@gmail.com"
					password = "Calito19941014"
					attendees =[correo,"juan.hernandez@bi-dss.com"]
					organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.hn.com"
					fro = "BANRURAL <citas_reclutamiento@banrural.hn.com>"

					ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

					#ddtstart = datetime.datetime.now()
					dtoff = datetime.timedelta(days = 1)
					dur = datetime.timedelta(hours = 1)
					ddtstart = ddtstart + dtoff
					ddtstart = ddtstart + datetime.timedelta(hours = 6)
					dtend = ddtstart + dur
					dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
					dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
					dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

					description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
					attendee = ""
					for att in attendees:
					   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
					ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
					ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
					ical+= "UID:FIXMEUID"+dtstamp+CRLF
					ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
					ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
					nombre = solicitud.nombres +" "+solicitud.primerapellido
					eml_body ='<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>,  a la dirección:  <b>'+ lugar +'</b>. Fecha y Hora: <b>'+ miFecha +'</b></p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p><br></div></div></div>'
					eml_body_bin = "This is the email body in binary - two steps"
					msg = MIMEMultipart('mixed')
					msg['Reply-To']=fro
					msg['Date'] = formatdate(localtime=True)
					msg['Subject'] = "Cita Programada con Candidato"
					msg['From'] = fro
					msg['To'] = ",".join(attendees)

					part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
					part_cal = MIMEText(ical,'calendar;method=REQUEST')

					msgAlternative = MIMEMultipart('alternative')
					msg.attach(msgAlternative)

					ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
					ical_atch.set_payload(ical)
					Encoders.encode_base64(ical_atch)
					ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

					eml_atch = MIMEBase('text/plain','')
					Encoders.encode_base64(eml_atch)
					eml_atch.add_header('Content-Transfer-Encoding', "")

					msgAlternative.attach(part_email)
					msgAlternative.attach(part_cal)

					mailServer = smtplib.SMTP('smtp.gmail.com', 587)
					mailServer.ehlo()
					mailServer.starttls()
					mailServer.ehlo()
					mailServer.login(login, password)
					mailServer.sendmail(fro, attendees, msg.as_string())
					mailServer.close()

					return redirect(reverse('seguimiento', kwargs={'codigo': aplicacion.Cod_aplicacion}))
			except Exception as e:
				raise

#2
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Examen_psico(request , codigo):

	if request.POST:
		with transaction.atomic():
			#try:
			aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
			solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)

			seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
			seguimiento.Pruebas_Psico = True
			seguimiento.Email = request.POST.get('Correo_pruebas')
			seguimiento.Contrasena = request.POST.get('Contrasena_pruebas')
			seguimiento.Fch_Pruebas_Psico = request.POST.get('Fecha_limite_pruebas')
			seguimiento.save()
			correo = solicitud.correo
			correoAnalista = request.user.email
			nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)

			correo_para_ingresar = request.POST.get('Correo_pruebas')
			contra = request.POST.get('Contrasena_pruebas')
			fecha = seguimiento.Fch_Pruebas_Psico
			nombre = seguimiento.Cod_Solicitud.nombres
			import mimetypes
			import smtplib
			from email.mime.multipart import MIMEMultipart
			from email.mime.text import MIMEText
			from email.MIMEBase import MIMEBase
			from email.Encoders import encode_base64

			if settings.EN_SERVIDOR == True:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> le asigne las evaluaciones en linea, para dar continuidad con el proceso de seleccion. <br> Pagina: <a href="https://rrhh.banrural.com.gt" target="_blank">Sistema de evaluacion</a> <br>luego debe dar en la opción: vaya a este sitio web (no recomendado). <br> CORREO ASIGNADO:<br> <b style="color: blue; font-weight: bold;">"'+correo_para_ingresar+'"</b> <br>CONTRASEÑA:<br> <b style="color: blue; font-weight: bold;">"'+contra+'"</b><br>Recuerde que tiene que estar concentrado (a) y sin distracciones; le adjunto el manual de uso del sistema. <br> Recordándole que para la evaluación de matemática no debe usar calculadora (papel y lápiz es lo que debe utilizar); estaremos monitoreando el avance de las mismas. <br> <b style="color: blue;">Intente realizarlo con internet explorer para que no tenga ningún inconveniente.</b> <br>Fecha limite: "'+fecha+'" <br><br>Saludos Cordiales</p><p style="color: red;">**Este correo es generico, no lo conteste**</p></section></div>'

				email_from = 'ReclutamientoRRHH@banrural.com.hn'
				email_to = [correo, correoAnalista]
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Evaluaciones en linea'
				msg['From'] = email_from
				msg['To'] = ' '.join(email_to) 

				path= settings.MEDIA_ROOT +'/File/MANUAL_DE_EVALUACION_ONLINE.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='MANUAL_DE_EVALUACION_ONLINE.pdf')
				msg.attach(adjunto)
				#msg.attach(getAttachment(file(settings.MEDIA_ROOT +'/File/MANUAL_DE_EVALUACION_ONLINE.pdf').read()))

				server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
				server.sendmail(email_from, email_to, msg.as_string())
				server.quit()
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			else:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia '+nombre+',<br> le asigne las evaluaciones en linea, para dar continuidad con el proceso de seleccion. <br> Pagina: <a href="https://rrhh.banrural.com.gt" target="_blank">Sistema de evaluacion</a> <br>luego debe dar en la opción: vaya a este sitio web (no recomendado). <br> CORREO ASIGNADO:<br> <b style="color: blue; font-weight: bold;">"'+correo_para_ingresar+'"</b> <br>CONTRASEÑA:<br> <b style="color: blue; font-weight: bold;">"'+contra+'"</b><br>Recuerde que tiene que estar concentrada y sin distracciones; le adjunto el manual de uso del sistema. <br> Recordándole que para la evaluación de matemática no debe usar calculadora (papel y lápiz es lo que debe utilizar); estaremos monitoreando el avance de las mismas. <br> <b style="color: blue;">Intente realizarlo con internet explorer para que no tenga ningún inconveniente.</b> <br>Fecha limite: "'+fecha+'" <br><br>Saludos Cordiales</p><p>Para consulta o dudas: <br> Correo electrónico: <b>'+correoAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p></section></div>'

				email_from = '900007@banrural.com.hn'
				email_to = correo
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Evaluaciones en linea'
				msg['From'] = email_from
				msg['To'] = email_to
				
				path= settings.MEDIA_ROOT +'/File/MANUAL_DE_EVALUACION_ONLINE.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='MANUAL_DE_EVALUACION_ONLINE.pdf')
				msg.attach(adjunto)
				#msg.attach(getAttachment(file(settings.MEDIA_ROOT +'/File/MANUAL_DE_EVALUACION_ONLINE.PDF').read()))
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
			return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			#except Exception as e:
				#raise

#3
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Entrevista_jefe(request , codigo):
	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)
		with transaction.atomic():
			try: 
				seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
				seguimiento.Jefe_Inme = True
				seguimiento.Fch_Jefe = request.POST.get('Entrevista_Jefe')
				#Se construye la fecha y hora dependiendo de los datos seleccionados
				if request.POST.get('Tiempo') == 'pm':
					fecha_hora = "%s %s:%s:00" % (request.POST.get('Entrevista_Jefe'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
				else:
					
					fecha_hora = "%s %s:%s:00" % (request.POST.get('Entrevista_Jefe'), request.POST.get('hora'), request.POST.get('minuto') )
				seguimiento.Hor_Jefe = fecha_hora
				seguimiento.save()

			except Exception as e:
				raise
		
		fecha = request.POST['Entrevista_Jefe']
		values_fecha = fecha.split("-")
		year= values_fecha[0]
		month= values_fecha[1]
		day= values_fecha[2]
		if request.POST.get('Tiempo') == 'pm':
			hora = (int(request.POST.get('hora')) + 12)
		else:
			hora = request.POST.get('hora')
		minuto = request.POST.get('minuto')
		from datetime import datetime
		dt= datetime(int(year), int(month), int(day), int(hora), int(minuto), 50)
		fechita= dt.strftime("%d/%m/%Y %I:%M %p")
		miFecha = str(fechita)
			
		lugar = " "
		#CORREO DE LA CITA
		import smtplib
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEBase import MIMEBase
		from email.MIMEText import MIMEText
		from email.Utils import COMMASPACE, formatdate
		from email import Encoders
		import datetime, os
		if settings.EN_SERVIDOR == True:
			CRLF = "\r\n"
			correouser = correoAnalista
			attendees =[correo,correouser]
			organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
			fro = "BANRURAL <citas_reclutamiento@banrural.com.hn>"

			ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
			#ddtstart = datetime.datetime.now()
			dtoff = datetime.timedelta(days = 1)
			dur = datetime.timedelta(hours = 1)
			ddtstart = ddtstart + dtoff
			ddtstart = ddtstart + datetime.timedelta(hours = 6)
			dtend = ddtstart + dur
			dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
			dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
			dtend = dtend.strftime("%Y%m%dT%H%M%SZ")
			description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
			attendee = ""
			for att in attendees:
			   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
			ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
			ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
			ical+= "UID:FIXMEUID"+dtstamp+CRLF
			ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
			ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
			nombre = solicitud.nombres +" "+solicitud.primerapellido
			eml_body = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="max-width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>, a la dirección: <b>'+ request.POST['direccion'] +'</b> .Fecha y Hora: <b>'+ miFecha +'</b></p><p style="color: red;">**Este correo es generico, no lo conteste**</p><br></div></div></div>'
			eml_body_bin = "This is the email body in binary - two steps"
			msg = MIMEMultipart('mixed')
			msg['Reply-To']=fro
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = "Entrevista con jefe inmediato"
			msg['From'] = fro
			msg['To'] = ",".join(attendees)

			part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
			part_cal = MIMEText(ical,'calendar;method=REQUEST')

			msgAlternative = MIMEMultipart('alternative')
			msg.attach(msgAlternative)

			ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
			ical_atch.set_payload(ical)
			Encoders.encode_base64(ical_atch)
			ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

			eml_atch = MIMEBase('text/plain','')
			Encoders.encode_base64(eml_atch)
			eml_atch.add_header('Content-Transfer-Encoding', "")

			msgAlternative.attach(part_email)
			msgAlternative.attach(part_cal)

			mailServer = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
			mailServer.ehlo()
			mailServer.sendmail(fro, attendees, msg.as_string())
			mailServer.close()
			return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))

		else:
			CRLF = "\r\n"
			login = "juancalihernandez@gmail.com"
			password = "Calito19941014"
			attendees =[correo,"juan.hernandez@bi-dss.com"]
			organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
			fro = "BANRURAL <citas_reclutamiento@banrural.hn.com>"

			ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
			#ddtstart = datetime.datetime.now()
			dtoff = datetime.timedelta(days = 1)
			dur = datetime.timedelta(hours = 1)
			ddtstart = ddtstart + dtoff
			ddtstart = ddtstart + datetime.timedelta(hours = 6)
			dtend = ddtstart + dur
			dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
			dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
			dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

			description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
			attendee = ""
			for att in attendees:
			   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
			ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
			ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
			ical+= "UID:FIXMEUID"+dtstamp+CRLF
			ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
			ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
			nombre = solicitud.nombres +" "+solicitud.primerapellido
			eml_body = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>,  a la dirección: <b>'+ lugar +'</b>. Fecha y Hora: <b>'+ miFecha+'</b></p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p><br></div></div></div>'
			eml_body_bin = "This is the email body in binary - two steps"
			msg = MIMEMultipart('mixed')
			msg['Reply-To']=fro
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = "Cita Programada con Candidato"
			msg['From'] = fro
			msg['To'] = ",".join(attendees)

			part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
			part_cal = MIMEText(ical,'calendar;method=REQUEST')

			msgAlternative = MIMEMultipart('alternative')
			msg.attach(msgAlternative)

			ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
			ical_atch.set_payload(ical)
			Encoders.encode_base64(ical_atch)
			ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

			eml_atch = MIMEBase('text/plain','')
			Encoders.encode_base64(eml_atch)
			eml_atch.add_header('Content-Transfer-Encoding', "")

			msgAlternative.attach(part_email)
			msgAlternative.attach(part_cal)

			mailServer = smtplib.SMTP('smtp.gmail.com', 587)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(login, password)
			mailServer.sendmail(fro, attendees, msg.as_string())
			mailServer.close()
			return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
				

#4
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Poligrafo(request , codigo):
	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)

		with transaction.atomic():
			#try:
			seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
			seguimiento.Poligrafo = True
			seguimiento.Fch_Poligrafo = request.POST.get('poligrafo_fecha')
			seguimiento.Dir_Poligrafo = request.POST.get('Direccion_Poligrafo')
			if request.POST.get('Tiempo') == 'pm':
				fecha_hora = "%s %s:%s:00" % (request.POST.get('poligrafo_fecha'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				fecha_hora = "%s %s:%s:00" % (request.POST.get('poligrafo_fecha'), request.POST.get('hora'), request.POST.get('minuto') )
			seguimiento.Hor_Poligrafo = fecha_hora
			seguimiento.save()

			lugar = " "

			fecha = request.POST['poligrafo_fecha']
			values_fecha = fecha.split("-")
			year= values_fecha[0]
			month= values_fecha[1]
			day= values_fecha[2]
			if request.POST.get('Tiempo') == 'pm':
				hora = (int(request.POST.get('hora')) + 12)
			else:
				hora = request.POST.get('hora')
			minuto = request.POST.get('minuto')
			from datetime import datetime
			dt= datetime(int(year), int(month), int(day), int(hora), int(minuto), 50)
			fechita= dt.strftime("%d/%m/%Y %I:%M %p")
			miFecha = str(fechita)

			#CORREO DE LA CITA
			import smtplib
			from email.MIMEMultipart import MIMEMultipart
			from email.MIMEBase import MIMEBase
			from email.MIMEText import MIMEText
			from email.Utils import COMMASPACE, formatdate
			from email import Encoders
			import os,datetime

			if settings.EN_SERVIDOR == True:

				CRLF = "\r\n"
				correouser = correoAnalista
				attendees =[correo,correouser]
				organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
				fro = "BANRURAL <citas_reclutamiento@banrural.com.hn>"

				ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

				#ddtstart = datetime.datetime.now()
				dtoff = datetime.timedelta(days = 1)
				dur = datetime.timedelta(hours = 1)
				ddtstart = ddtstart + dtoff
				ddtstart = ddtstart + datetime.timedelta(hours = 6)
				dtend = ddtstart + dur
				dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
				dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
				dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

				description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
				attendee = ""
				for att in attendees:
				   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
				ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
				ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
				ical+= "UID:FIXMEUID"+dtstamp+CRLF
				ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
				ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
				nombre = solicitud.nombres +" "+solicitud.primerapellido
				direccion = request.POST.get('Direccion_Poligrafo')
				eml_body = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>, <br> a la dirección <b>'+ request.POST.get('Direccion_Poligrafo')+'</b>.<br> Fecha y Hora: <b>'+ miFecha +'</b></p><p style="color: red;">**Este correo es generico, no lo conteste**</p><br></div></div></div>'
				eml_body_bin = "This is the email body in binary - two steps"
				msg = MIMEMultipart('mixed')
				msg['Reply-To']=fro
				msg['Date'] = formatdate(localtime=True)
				msg['Subject'] = "Poligrafo"
				msg['From'] = fro
				msg['To'] = ",".join(attendees)
				part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
				part_cal = MIMEText(ical,'calendar;method=REQUEST')

				msgAlternative = MIMEMultipart('alternative')
				msg.attach(msgAlternative)

				ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
				ical_atch.set_payload(ical)
				Encoders.encode_base64(ical_atch)
				ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

				eml_atch = MIMEBase('text/plain','')
				Encoders.encode_base64(eml_atch)
				eml_atch.add_header('Content-Transfer-Encoding', "")

				msgAlternative.attach(part_email)
				msgAlternative.attach(part_cal)

				mailServer = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
				mailServer.ehlo()
				mailServer.sendmail(fro, attendees, msg.as_string())
				mailServer.close()
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			else:
				CRLF = "\r\n"
				login = "juancalihernandez@gmail.com"
				password = "Calito19941014"
				attendees =[correo,correoAnalista]
				organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
				fro = "BANRURAL <citas_reclutamiento@banrural.hn.com>"

				ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

				#ddtstart = datetime.datetime.now()
				dtoff = datetime.timedelta(days = 1)
				dur = datetime.timedelta(hours = 1)
				ddtstart = ddtstart + dtoff
				ddtstart = ddtstart + datetime.timedelta(hours = 6)
				dtend = ddtstart + dur
				dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
				dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
				dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

				description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
				attendee = ""
				for att in attendees:
				   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
				ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
				ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
				ical+= "UID:FIXMEUID"+dtstamp+CRLF
				ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
				ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
				nombre = solicitud.nombres +" "+solicitud.primerapellido
				direccion = request.POST.get('Direccion_Poligrafo')
				eml_body = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p>Se acaba de ingresar una cita con el candidato: <b>'+ nombre +'</b>, <br> a la dirección <b>'+ lugar+'</b>.<br> Fecha y Hora: <b>'+ miFecha +'</b></p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p><p>Este correo es generico, no lo conteste</p><br></div></div></div>'
				eml_body_bin = "This is the email body in binary - two steps"
				msg = MIMEMultipart('mixed')
				msg['Reply-To']=fro
				msg['Date'] = formatdate(localtime=True)
				msg['Subject'] = "Cita Programada con Candidato"
				msg['From'] = fro
				msg['To'] = ",".join(attendees)
				part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
				part_cal = MIMEText(ical,'calendar;method=REQUEST')

				msgAlternative = MIMEMultipart('alternative')
				msg.attach(msgAlternative)

				ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
				ical_atch.set_payload(ical)
				Encoders.encode_base64(ical_atch)
				ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

				eml_atch = MIMEBase('text/plain','')
				Encoders.encode_base64(eml_atch)
				eml_atch.add_header('Content-Transfer-Encoding', "")

				msgAlternative.attach(part_email)
				msgAlternative.attach(part_cal)

				mailServer = smtplib.SMTP('smtp.gmail.com', 587)
				mailServer.ehlo()
				mailServer.starttls()
				mailServer.ehlo()
				mailServer.login(login, password)
				mailServer.sendmail(fro, attendees, msg.as_string())
				mailServer.close()

				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			#except Exception as e:
				#raise

#5
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def socio(request , codigo):
	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)
		with transaction.atomic():
			#try:
			seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
			seguimiento.Socio_Econ = True
			seguimiento.Fch_Socio = request.POST.get('visita_fecha')
			if request.POST.get('Tiempo') == 'pm':
				fecha_hora = "%s %s:%s:00" % (request.POST.get('visita_fecha'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				fecha_hora = "%s %s:%s:00" % (request.POST.get('visita_fecha'), request.POST.get('hora'), request.POST.get('minuto') )
			seguimiento.Hor_Socio = fecha_hora
			seguimiento.save()
			nombre = solicitud.nombres +" "+solicitud.primerapellido
			lugar = " "

			fecha = request.POST['visita_fecha']
			values_fecha = fecha.split("-")
			year= values_fecha[0]
			month= values_fecha[1]
			day= values_fecha[2]
			if request.POST.get('Tiempo') == 'pm':
				hora = (int(request.POST.get('hora')) + 12)
			else:
				hora = request.POST.get('hora')
			minuto = request.POST.get('minuto')
			from datetime import datetime
			dt= datetime(int(year), int(month), int(day), int(hora), int(minuto), 50)
			fechita= dt.strftime("%d/%m/%Y %I:%M %p")
			miFecha = str(fechita)

			#CORREO DE LA CITA
			import smtplib
			from email.MIMEMultipart import MIMEMultipart
			from email.MIMEBase import MIMEBase
			from email.MIMEText import MIMEText
			from email.Utils import COMMASPACE, formatdate
			from email import Encoders
			import os,datetime

			if settings.EN_SERVIDOR == True:
				CRLF = "\r\n"
				correouser = str(request.user.email)
				attendees =[correo,correouser]

				organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.com.hn"
				fro = "BANRURAL <citas_reclutamiento@banrural.com.hn>"

				ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

				#ddtstart = datetime.datetime.now()
				dtoff = datetime.timedelta(days = 1)
				dur = datetime.timedelta(hours = 1)
				ddtstart = ddtstart + dtoff
				ddtstart = ddtstart + datetime.timedelta(hours = 6)
				dtend = ddtstart + dur
				dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
				dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
				dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

				description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
				attendee = ""
				for att in attendees:
				   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
				ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
				ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
				ical+= "UID:FIXMEUID"+dtstamp+CRLF
				ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
				ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
				
				eml_body = "<div style='width: 100%; padding-left: 10px;'><div class='contenedor' style='width: 500px; '><div class='header' style='text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;'><h1  style='color: #00853F; font-weight: 500;'>Reclutamiento Banrural</h1></div><section style='text-align: left; margin-left:5px;'><p> Se acaba de ingresar una cita con el candidato <b>"+nombre+"</b>, </p><p>a la direccion: <b>"+request.POST['direccion']+".</b></p><p>Fecha y Hora: <b>"+miFecha+"</b></p><p style='color: red;'>**Este correo es generico, no lo conteste**</p></section></div></div>"
				eml_body_bin = "This is the email body in binary - two steps"
				msg = MIMEMultipart('mixed')
				msg['Reply-To']=fro
				msg['Date'] = formatdate(localtime=True)
				msg['Subject'] = "Estudio socio-económico"
				msg['From'] = fro
				msg['To'] = ",".join(attendees)
				part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
				part_cal = MIMEText(ical,'calendar;method=REQUEST')

				msgAlternative = MIMEMultipart('alternative')
				msg.attach(msgAlternative)

				ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
				ical_atch.set_payload(ical)
				Encoders.encode_base64(ical_atch)
				ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

				eml_atch = MIMEBase('text/plain','')
				Encoders.encode_base64(eml_atch)
				eml_atch.add_header('Content-Transfer-Encoding', "")

				msgAlternative.attach(part_email)
				msgAlternative.attach(part_cal)



				mailServer = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
				mailServer.ehlo()
				mailServer.sendmail(fro, attendees, msg.as_string())
				mailServer.close()
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))

			else:
				CRLF = "\r\n"
				login = "juancalihernandez@gmail.com"
				password = "Calito19941014"
				attendees =[correo,"juan.hernandez@bi-dss.com"]
				organizer = "ORGANIZER;CN=BANRURAL:mailto:citas"+CRLF+" @banrural.hn.com"
				fro = "BANRURAL <citas_reclutamiento@banrural.hn.com>"

				ddtstart = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

				#ddtstart = datetime.datetime.now()
				dtoff = datetime.timedelta(days = 1)
				dur = datetime.timedelta(hours = 1)
				ddtstart = ddtstart + dtoff
				ddtstart = ddtstart + datetime.timedelta(hours = 6)
				dtend = ddtstart + dur
				dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
				dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
				dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

				description = "DESCRIPTION: Nueva Cita Ingresada"+CRLF
				attendee = ""
				for att in attendees:
				   attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
				ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
				ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
				ical+= "UID:FIXMEUID"+dtstamp+CRLF
				ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+lugar+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
				ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
				
				eml_body = "<div style='width: 100%; padding-left: 10px;'><div class='contenedor' style='width: 500px; '><div class='header' style='text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;'><h1  style='color: #00853F; font-weight: 500;'>Reclutamiento Banrural</h1></div><section style='text-align: left; margin-left:5px;'><p> Se acaba de ingresar una cita con el candidato <b>"+nombre+"</b>, </p><p>a la direccion: <b>"+lugar+".</b></p><p>Fecha y Hora: <b>"+miFecha+"</b></p><p>Para consulta o dudas: <br> Correo electrónico:<b>"+correoAnalista+"</b> <br>Teléfono: <b>"+telefonoAnalista+"</b> Extensión: <b>"+extensionAnalista+"</b><br> Con: <b>"+nombreAnalista+"</b></p></section></div></div>"
				eml_body_bin = "This is the email body in binary - two steps"
				msg = MIMEMultipart('mixed')
				msg['Reply-To']=fro
				msg['Date'] = formatdate(localtime=True)
				msg['Subject'] = "Cita Programada con Candidato"
				msg['From'] = fro
				msg['To'] = ",".join(attendees)
				part_email = MIMEText(eml_body.encode('utf-8'), 'html', 'utf-8')
				part_cal = MIMEText(ical,'calendar;method=REQUEST')

				msgAlternative = MIMEMultipart('alternative')
				msg.attach(msgAlternative)

				ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
				ical_atch.set_payload(ical)
				Encoders.encode_base64(ical_atch)
				ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

				eml_atch = MIMEBase('text/plain','')
				Encoders.encode_base64(eml_atch)
				eml_atch.add_header('Content-Transfer-Encoding', "")

				msgAlternative.attach(part_email)
				msgAlternative.attach(part_cal)

				mailServer = smtplib.SMTP('smtp.gmail.com', 587)
				mailServer.ehlo()
				mailServer.starttls()
				mailServer.ehlo()
				mailServer.login(login, password)
				mailServer.sendmail(fro, attendees, msg.as_string())
				mailServer.close()

				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			#except Exception as e:
				#raise

#6
@login_required()
@permission_required('admin.ver_admin')
@transaction.atomic
def Doc(request , codigo):

	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		telefonoAnalista = request.POST['txtTelefono']
		extensionAnalista = request.POST['txtExtension']
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)

		with transaction.atomic():
			#try:
			seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
			seguimiento.Documentacion = True
			seguimiento.Fch_Doc = request.POST.get('Fecha_Limite')
			seguimiento.save()

			nombre = solicitud.nombres +" "+solicitud.primerapellido
			fecha = request.POST.get('Fecha_Limite')
			import mimetypes
			import smtplib
			from email.mime.multipart import MIMEMultipart
			from email.mime.text import MIMEText
			from email.MIMEBase import MIMEBase
			from email.Encoders import encode_base64

			if settings.EN_SERVIDOR == True:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> Para poder proceder con el proceso de selección a la plaza que está participando actualmente, solicito su apoyo gestionando la documentación pertinente al proceso. Adjunto encontrara la lista de documentación solicitada,<br> <b style="font-style: italic; text-decoration: underline;">Tienen hasta "'+fecha+'" a las 2:00 p.m.</b> para presentar toda la documentación.<br>Saludos Cordiales</p> <p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p> <p style="color: red;">**Este correo es generico, no lo conteste**</p></section></div>'

				email_from = 'ReclutamientoRRHH@banrural.com.hn'
				email_to = [correo, correoAnalista]
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Documentación'
				msg['From'] = email_from
				msg['To'] = ",".join(email_to) 

				path= settings.MEDIA_ROOT +'/File/REQUISITOS_BANRURAL.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='REQUISITOS_BANRURAL.pdf')
				msg.attach(adjunto)

				server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
				server.sendmail(email_from, email_to, msg.as_string())
				server.quit()
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			else:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> Para poder proceder con el proceso de selección a la plaza que está participando actualmente, solicito su apoyo gestionando la documentación pertinente al proceso. Adjunto encontrara la lista de documentación solicitada,<br> <b style="font-style: italic; text-decoration: underline;">Tienen hasta "'+fecha+'" a las 2:00 p.m.</b> para juntar toda la documentación.<br>Saludos Cordiales</p> <p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p></section></div>'

				email_from = '900007@banrural.com.hn'
				email_to = correo
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Documentación'
				msg['From'] = email_from
				msg['To'] = email_to
				
				path= settings.MEDIA_ROOT +'/File/REQUISITOS_BANRURAL.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='REQUISITOS_BANRURAL.pdf')
				msg.attach(adjunto)
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
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			#except Exception as e:
				#raise

#7
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Medicos(request, codigo):
	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		correo = solicitud.correo
		correoAnalista = request.user.email
		nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)

		with transaction.atomic():
			#try:
			seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
			seguimiento.Medicos = True
			seguimiento.Fch_Medicos = request.POST.get('Fecha_medicos')
			seguimiento.Dir_Medicos = request.POST.get('Direccion_Examenes')

			if request.POST.get('Tiempo') == 'pm':
				fecha_hora = "%s %s:%s:00" % (request.POST.get('Fecha_medicos'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				fecha_hora = "%s %s:%s:00" % (request.POST.get('Fecha_medicos'), request.POST.get('hora'), request.POST.get('minuto') )
			
			seguimiento.Hor_Medicos = fecha_hora
			seguimiento.save()

			fecha = request.POST['Fecha_medicos']
			values_fecha = fecha.split("-")
			year= values_fecha[0]
			month= values_fecha[1]
			day= values_fecha[2]
			if request.POST.get('Tiempo') == 'pm':
				hora = (int(request.POST.get('hora')) + 12)
			else:
				hora = request.POST.get('hora')
			minuto = request.POST.get('minuto')
			from datetime import datetime
			dt= datetime(int(year), int(month), int(day), int(hora), int(minuto), 50)
			fechita= dt.strftime("%d/%m/%Y %I:%M %p")
			miFecha = str(fechita)

			nombre = solicitud.nombres +" "+solicitud.primerapellido
			fecha = request.POST.get('Fecha_Limite')
			direccion = " "
			import mimetypes
			import smtplib
			from email.mime.multipart import MIMEMultipart
			from email.mime.text import MIMEText
			from email.MIMEBase import MIMEBase
			from email.Encoders import encode_base64

			if settings.EN_SERVIDOR == True:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> Para poder continuar con el proceso de selección de la plaza a la que está aplicando actualmente, solicito su apoyo gestionando la documentación pertinente al proceso. Adjunto encontrara la autorizacion de examen medico,<br> necesito imprima la autorización, la llene y me la haga llegar mediante fotografía (clara y leíble) o escaneada, a más tardar el día <b style="font-style: italic; text-decoration: underline;">"'+miFecha+'" </b>.</p> <p>Dirección para los exámenes médicos: <b style="font-style: italic; text-decoration: underline;">'+request.POST.get('Direccion_Examenes')+' </b></p> <p>Saludos Cordiales</p><p style="color: red;">**Este correo es generico, no lo conteste**</p></section></div></div>'

				email_from = 'ReclutamientoRRHH@banrural.com.hn'
				email_to = [correo,correoAnalista]
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Autorización de exámenes medicos'
				msg['From'] = email_from
				msg['To'] = ",".join(email_to)

				path= settings.MEDIA_ROOT +'/File/AUTORIZACION_EXAMEN_MEDICO.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='AUTORIZACION_EXAMEN_MEDICO.pdf')
				msg.attach(adjunto)

				server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
				server.sendmail(email_from, email_to, msg.as_string())
				server.quit()
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			else:
				contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> Para poder proceder con el proceso de selección de las plazas a las que está participando actualmente, solicito su apoyo gestionando la documentación pertinente al proceso. Adjunto encontrara la autorizacion de examen medico,<br> necesito imprima la utorización Medica, la llenen y me la hagan llegar mediante fotografía (clara y leíble) o por escáner, a más tardar el día <b style="font-style: italic; text-decoration: underline;">"'+miFecha+'" </b>.<br>Saludos Cordiales</p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p></section></div></div>'

				email_from = '900007@banrural.com.hn'
				email_to = correo
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Autorización de exámenes medicos'
				msg['From'] = email_from
				msg['To'] = email_to
				
				path= settings.MEDIA_ROOT +'/File/AUTORIZACION_EXAMEN_MEDICO.pdf'
				msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
				fp = open(path,'rb')
				adjunto = MIMEBase('multipart', 'encrypted')
				adjunto.set_payload(fp.read()) 
				fp.close()  
				encode_base64(adjunto) 
				adjunto.add_header('Content-Disposition', 'attachment', filename='AUTORIZACION_EXAMEN_MEDICO.pdf')
				msg.attach(adjunto)
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
				return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
			#except Exception as e:
				#raise

#8
@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def CC(request , codigo):
	if request.POST:
		aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
		solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk)
		with transaction.atomic():
			try:
				seguimiento = SeguimientoXAplicacion.objects.get(Cod_Aplicacion = codigo)
				seguimiento.CC =True
				seguimiento.Fch_Ingreso = request.POST.get('Fecha_Ingreso')
				seguimiento.save()
				fechaComienzo = request.POST['Fecha_Comienzo']

				from datetime import datetime
				fecha = request.POST['Fecha_Ingreso']
				values_fecha = fecha.split("-")
				year= values_fecha[0]
				month= values_fecha[1]
				day= values_fecha[2]
				dt= datetime(int(year), int(month), int(day))			
				fechaDiaAntes = dt.strftime('%d/%m/%Y')
				fechaDiaAntes = str(fechaDiaAntes) 

				fecha = request.POST['Fecha_Comienzo']
				values_fecha = fecha.split("-")
				year= values_fecha[0]
				month= values_fecha[1]
				day= values_fecha[2]
				dt= datetime(int(year), int(month), int(day))			
				fechaDiaInicio = dt.strftime('%d/%m/%Y')
				fechaDiaInicio = str(fechaDiaInicio) 

				nombre = solicitud.nombres +" "+solicitud.primerapellido
				correo = solicitud.correo
				correoAnalista = request.user.email
				nombreAnalista = str(request.user.first_name)+ " "+str(request.user.last_name)
				import mimetypes
				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText
				from email.MIMEBase import MIMEBase
				from email.Encoders import encode_base64

				if settings.EN_SERVIDOR == True:
					contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="max-width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">Reclutamiento Banrural</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">Feliz dia: <b>'+nombre+'.</b></p><p style="color: #201d33;  font-size: 18px;">Le detallo cómo será el trámite para su ingreso:</p><p>El día <b>'+fechaDiaInicio+'</b> se dará inicio a las capacitaciones Banrural, deberán viajar el <b>'+fechaDiaAntes+'</b> a Tegucigalpa para poder hospedarse en el centro de capacitación y la hora de ingreso es: 03:00 p.m. (Si tienen inconvenientes para dar con la dirección pueden llamar al 2290-1010 ext. 499434)</p><p>En el caso que viva en Tegucigalpa usted se deberá presentar el <b>'+fechaDiaInicio+'</b> a las 07:30 a.m. (Si tienen inconvenientes para dar con la dirección pueden llamar al 2290-1010 ext. 499434)</p><p style="background-color: yellow;">Dirección del Centro de Capacitación: Comayagüela entre 1 y 2 avenida esquina opuesta a galería bellas artes, frente a parqueo de banco de los trabajadores, entrar por la puerta pequeña que esta polarizada (Permanece cerrado por favor tocar la puerta para que el guardia les pueda abrir)</p><p style=" text-decoration-line: underline;">IMPORTANTE TOMAR EN CUENTA LO SIGUIENTE:</p><ol><li><p>Traer copia de las Identidades de las personas que van a ingresar al seguro de vida ( solo abarca esposa (o) e hijos) y si son menores de edad copia de las partidas de nacimiento.</p></li><li><p>Traer copia de las Identidades de las personas que van a ingresar como beneficiarios del RAP y si son menores de edad copia de las partidas de nacimiento.</p></li<li><p>Deben presentar toda la documentación original aunque la hayan enviado escaneada.</p></li><li><p>Los Antecedentes Penales y Policiales estos son originales</p></li><li><p>Traer dos fotografías tamaño carnet.</p></li></ol><p style="background-color: yellow;">NOTA: SI ALGUIEN TIENE DOCUMENTOS PENDIENTES TODAVIA POR FAVOR PRESENTARLOS EL DIA <b>'+fechaDiaInicio+'</b>, DE LO CONTRARIO SE RETIRARA DEL CENTRO DE CAPACITACION.</p><p>Le adjunto un documento donde se le explica lo que puede traer para la capacitación.</p><p style="color: red;">**Este correo es generico, no lo conteste**</p><br></div></div></div>'
					
					email_from = 'ReclutamientoRRHH@banrural.com.hn'
					email_to = [correo,correoAnalista]
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'INGRESO A CENTRO DE CAPACITACION'
					msg['From'] = email_from
					msg['To'] = ",".join(email_to)

					path= settings.MEDIA_ROOT +'/File/INFORMACION_PARA_INDUCCION_HONDURAS.pdf'
					msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
					fp = open(path,'rb')
					adjunto = MIMEBase('multipart', 'encrypted')
					adjunto.set_payload(fp.read()) 
					fp.close()  
					encode_base64(adjunto) 
					adjunto.add_header('Content-Disposition', 'attachment', filename='INFORMACION_PARA_INDUCCION_HONDURAS.pdf')
					msg.attach(adjunto)

					server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
					server.sendmail(email_from, email_to, msg.as_string())
					server.quit()
					return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
				else:
					contenido_html = '<div style="padding-left: 10px; width: 100%;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #F68E1E;"><h1  style="color: #00853F; font-weight: 500;">Reclutamiento Banrural</h1></div><section style="text-align: left; margin-left:5px;" ><p>Feliz dia "'+nombre+'",<br> Para poder proceder con el proceso de selección de las plazas a las que está participando actualmente, solicito su apoyo gestionando la documentación pertinente al proceso. Adjunto encontrara la autorizacion de examen medico,<br> necesito imprima la utorización Medica, la llenen y me la hagan llegar mediante fotografía (clara y leíble) o por escáner, a más tardar el día <b style="font-style: italic; text-decoration: underline;">"'+miFecha+'" </b>.<br>Saludos Cordiales</p><p>Para consulta o dudas: <br> Correo electrónico:<b>'+correoAnalista+'</b> <br>Teléfono: <b>'+telefonoAnalista+'</b> Extensión: <b>'+extensionAnalista+'</b><br> Con: <b>'+nombreAnalista+'</b></p></section></div></div>'

					email_from = '900007@banrural.com.hn'
					email_to = correo
					msg = MIMEMultipart('alternative')
					msg['Subject'] = 'INGRESO A CENTRO DE CAPACITACION'
					msg['From'] = email_from
					msg['To'] = email_to
					
					path= settings.MEDIA_ROOT +'/File/AUTORIZACION_EXAMEN_MEDICO.pdf'
					msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
					fp = open(path,'rb')
					adjunto = MIMEBase('multipart', 'encrypted')
					adjunto.set_payload(fp.read()) 
					fp.close()  
					encode_base64(adjunto) 
					adjunto.add_header('Content-Disposition', 'attachment', filename='AUTORIZACION_EXAMEN_MEDICO.pdf')
					msg.attach(adjunto)
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
					return redirect(reverse('seguimiento', kwargs={'codigo': seguimiento.Cod_Aplicacion.pk}))
				
			except Exception as e:
				raise e

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic
def Citas(request):
	import datetime
	fecha = datetime.date.today()
	primera_cita = SeguimientoXAplicacion.objects.filter(Fch_Pr_Entrevista= fecha)
	pruebas_psico = SeguimientoXAplicacion.objects.filter(Fch_Pruebas_Psico= fecha)
	entre_jefe = SeguimientoXAplicacion.objects.filter(Fch_Jefe=fecha)
	poligrafo = SeguimientoXAplicacion.objects.filter(Fch_Poligrafo=fecha)
	doc = SeguimientoXAplicacion.objects.filter(Fch_Doc=fecha)
	
	if request.POST:
		metodo = request.POST['metodo']

		if metodo == '1':
			fech = request.POST.get('filtrar')
			primera_cita = SeguimientoXAplicacion.objects.filter(Fch_Pr_Entrevista= fech)
			pruebas_psico = SeguimientoXAplicacion.objects.filter(Fch_Pruebas_Psico= fech)
			entre_jefe = SeguimientoXAplicacion.objects.filter(Fch_Jefe=fech)
			poligrafo = SeguimientoXAplicacion.objects.filter(Fch_Poligrafo=fech)
			doc = SeguimientoXAplicacion.objects.filter(Fch_Doc=fech)
			ctx = {'primera_cita':primera_cita,
		 		'pruebas_psico':pruebas_psico,
		 		'entre_jefe':entre_jefe,
		 		'poligrafo': poligrafo,
		 		'doc':doc }
			return render(request, 'citas.html' , ctx)
		elif metodo == '2':
			fechaIncio = request.POST['TxtFchInicio']
			fechaFinal = request.POST['TxtFchFinal']
			primera_cita = SeguimientoXAplicacion.objects.filter(Fch_Pr_Entrevista__gte= fechaIncio, Fch_Pr_Entrevista__lte =fechaFinal  )
			pruebas_psico = SeguimientoXAplicacion.objects.filter(Fch_Pruebas_Psico__gte= fechaIncio, Fch_Pruebas_Psico__lte =fechaFinal )
			entre_jefe = SeguimientoXAplicacion.objects.filter(Fch_Jefe__gte=fechaIncio ,Fch_Jefe__lte = fechaFinal )
			poligrafo = SeguimientoXAplicacion.objects.filter(Fch_Poligrafo__gte=fechaIncio ,Fch_Poligrafo__lte = fechaFinal )
			doc = SeguimientoXAplicacion.objects.filter(Fch_Doc__gte=fechaIncio , Fch_Doc__lte= fechaFinal )
			ctx = {'primera_cita':primera_cita,
		 		'pruebas_psico':pruebas_psico,
		 		'entre_jefe':entre_jefe,
		 		'poligrafo': poligrafo,
		 		'doc':doc }
			return render(request, 'citas.html' , ctx)

		else:
			year = request.POST['years']
			mes = request.POST['meses']
			fecha = str(year+'-'+mes+'-01')
			primera_cita = SeguimientoXAplicacion.objects.filter(Fch_Pr_Entrevista__gte=fecha)
			pruebas_psico = SeguimientoXAplicacion.objects.filter(Fch_Pruebas_Psico__gte=fecha)
			entre_jefe = SeguimientoXAplicacion.objects.filter(Fch_Jefe__gte=fecha)
			poligrafo = SeguimientoXAplicacion.objects.filter(Fch_Poligrafo__gte=fecha)
			doc = SeguimientoXAplicacion.objects.filter(Fch_Doc__gte=fecha)
			ctx = {'primera_cita':primera_cita,
		 		'pruebas_psico':pruebas_psico,
		 		'entre_jefe':entre_jefe,
		 		'poligrafo': poligrafo,
		 		'doc':doc }
			return render(request, 'citas.html' , ctx)


	ctx = {'primera_cita':primera_cita,
	 'pruebas_psico':pruebas_psico,
	 'entre_jefe':entre_jefe,
	 'poligrafo': poligrafo,
	 'doc':doc }
	return render(request, 'citas.html' , ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
@transaction.atomic 
def visto(request, codigo):
	request.session['visto'] = Aplicaciones.objects.get(Cod_aplicacion = codigo).Cod_oferta.pk
	
	with transaction.atomic():
		try:
			aplicaciones = Aplicaciones.objects.get(Cod_aplicacion = codigo)
			aplicaciones.Visto = True
			aplicaciones.save()
			return redirect(reverse('perfil_candidato', kwargs={'solicitud': aplicaciones.Cod_solicitud.codsolicitud}))
		except Exception as e:
			raise

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def mensaje_gracias(request, codigo):
	usuario = User.objects.get(pk = request.user.id)
	Aplicaciones.objects.filter(Cod_aplicacion = codigo).update(Dislike = True , Favorito = False , codUser = usuario )
	aplicacion = Aplicaciones.objects.get(Cod_aplicacion = codigo)
	solicitud = Solicitud.objects.get(codsolicitud = aplicacion.Cod_solicitud.pk).correo
	oferta = Ofertas.objects.get(pk = aplicacion.Cod_oferta.pk)
	NombrePlaza = oferta.Puesto_oferta
	codigoOferta = oferta.pk
	import mimetypes
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.MIMEBase import MIMEBase
	from email.Encoders import encode_base64

	if settings.EN_SERVIDOR == True:
		contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">RECUTAMIENTO BANRURAL</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">Gracias por haber aplicado a la plaza : <b>'+NombrePlaza+'.</b> </p><p style="color: #201d33;  font-size: 18px;">Estimado candidato, <br> Agradecemos tu interés en formar parte de nuestra institución, en este momento tu perfil no aplica a  las plazas que tenemos vacantes, pero tus  datos  ya están ingresados en nuestra base, para próximas oportunidades.</p><p><b>Este correo es generico, no lo conteste</b></p></div></div></div>'
		email_to = solicitud
		email_from = 'ReclutamientoRRHH@banrural.com.hn'
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Gracias por haber aplicado'
		msg['From'] = email_from
		#msg['To'] = ', '.join(email_to)
		msg.attach(MIMEText(contenido_html.encode('utf-8'), 'html', 'utf-8'))
		server = smtplib.SMTP('banrural-com-hn.mail.protection.outlook.com:25')
		server.sendmail(email_from, email_to, msg.as_string())
		server.quit()

	else:
		contenido_html = '<div style="margin: 40px; text-align: center;"><div class="contenedor" style="width: 500px; "><div class="header" style=" text-align:center; padding:0px 15px ; border-bottom: 1px solid #e8a043;"><h1  style="color: #47963a; font-weight: 500;">RECUTAMIENTO BANRURAL</h1></div><div class="body" style="text-align: left; padding: 15px;"><p style="color: #201d33;  font-size: 18px;">Gracias por haber aplicado a la plaza : <b>'+NombrePlaza+'.</b> </p><p style="color: #201d33;  font-size: 18px;">No has sido seleccionado en esta ocación para optar a la plaza antes mencionada.</p><p style="color: #201d33;  font-size: 18px;">Éxitos</p></div></div></div>'

		email_from = '900007@banrural.com.hn'
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Nueva Oferta de Trabajo'
		msg['From'] = email_from
		#msg['To'] = ', '.join(email_to)
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

	return redirect(reverse('candidatos_plaza', kwargs={'codigo': codigoOferta}))

######################## GENERAR PDF's #################################

def PDFCitas(request):
	import datetime
	fecha = datetime.date.today()
	date = datetime.datetime.today()
	#primera_cita = SeguimientoXAplicacion.objects.all()
	primera_cita = SeguimientoXAplicacion.objects.filter(Fch_Pr_Entrevista = fecha)
	entre_jefe = SeguimientoXAplicacion.objects.filter(Fch_Jefe=fecha)
	#entre_jefe = SeguimientoXAplicacion.objects.all()
	data ={
		'date':date,
		'primera_cita':primera_cita,
		'entre_jefe':entre_jefe
	}
	try:
		pdf = render_to_pdf('pdfcitas.html', data)
		return HttpResponse(pdf, content_type='application/pdf')
	except Exception as e:
		pdf = render_to_pdf('pdfcitas.html', data)
		return HttpResponse(pdf, content_type='application/pdf')
	pdf = render_to_pdf('pdfcitas.html', data)
	return HttpResponse(pdf, content_type='application/pdf')

class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		codsolicitud = self.kwargs['solicitud']
		codaplicacion = self.kwargs['aplicacion']

		Aplicaciones.objects.filter(Cod_aplicacion = codaplicacion).update(Imprimir = True)
		
		solicitud = Solicitud.objects.get(codsolicitud=codsolicitud)
		data = {'solicitud':solicitud}
		try:
			lista_organizaciones = Organizacion.objects.filter(cod_solicitud=solicitud.codsolicitud)
			lista_cuentas = Cuenta.objects.filter(cod_solicitud=solicitud)
			lista_estudios = Historialacademico.objects.filter(codsolicitud=solicitud)
			lista_cursos = Curso.objects.filter(codsolicitud=solicitud)
			lista_idiomas = Idioma.objects.filter(cod_solicitud=solicitud)
			lista_habilidades = Habilidad.objects.filter(cod_solicitud=solicitud)
			lista_competencias = Competencia.objects.filter(cod_solicitud=solicitud)
			hermano = Hermano.objects.filter(codsolicitud=codsolicitud)
			hijo = Hijo.objects.filter(codsolicitud=codsolicitud)
			depen = Dependiente.objects.filter(codsolicitud=codsolicitud)
			laboral = Historiallaboral.objects.values().filter(codsolicitud=codsolicitud)
			personal = Referenciaspersonal.objects.values().filter(codsolicitud=codsolicitud)
			rlaboral = Referencia.objects.values().filter(codsolicitud=codsolicitud)
			data['hermano']=hermano
			data['hijo']=hijo
			data['depen']=depen
			data['laboral']=laboral
			data['personal']=personal
			data['rlaboral']=rlaboral
			data['lista_organizaciones'] = lista_organizaciones
			data['lista_cuentas'] = lista_cuentas
			data['lista_estudios'] = lista_estudios
			data['lista_cursos'] = lista_cursos
			data['lista_idiomas'] = lista_idiomas
			data['lista_habilidades'] = lista_habilidades
			data['lista_competencias'] = lista_competencias
			return render(request, 'index.html', data)
			#pdf = render_to_pdf('index.html', data)
			#return HttpResponse(pdf, content_type='application/pdf')
		except Exception as e:
			pdf = render_to_pdf('index.html', data)
			return HttpResponse(pdf, content_type='application/pdf')
		pdf = render_to_pdf('index.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def plazas_aplicado(request, codigo):
	lista_ofertas = Ofertas.objects.values('Cod_oferta', 'Puesto_oferta', 'Fecha_publicacion', 'Publica', 'Interna').filter(Estado = True)
	lista_plazas = Aplicaciones.objects.filter(Cod_solicitud = codigo)
	solicitud = Solicitud.objects.get(codsolicitud=codigo)


	if request.POST:
		with transaction.atomic():
			try:
				codigo_oferta = request.POST['plazaCBX']
				codigo_sol = request.POST['candidato']
				solicitud = Solicitud.objects.get(pk = codigo_sol)

				if not Aplicaciones.objects.filter(Cod_solicitud= codigo_sol, Cod_oferta = codigo_oferta ).count() >= 1 and solicitud.vista == 7:
					aplicacion = Aplicaciones()
					aplicacion.Cod_oferta = Ofertas.objects.get(Cod_oferta = codigo_oferta)
					aplicacion.Cod_solicitud = solicitud
					aplicacion.save()

					preguntas =Preguntas.objects.filter(Cod_oferta = codigo_oferta).values_list('Cod_pregunta', flat= True)
					for x in preguntas:
						respuesta = Respuestas()
						pre = Preguntas.objects.get(Cod_pregunta = x)
						respuesta.Cod_pregunta = pre
						respuesta.Descripcion_pregunta = pre.Descripcion_pregunta
						respuesta.Cod_solicitud = soli
						respuesta.Cod_aplicacion = aplicacion
						respuesta.Cod_oferta = Ofertas.objects.get(Cod_oferta = codigo)
						respuesta.Descripcion_respuesta = "-----"
						respuesta.save()
			except Exception as e:
				print 'errror',e

		lista_ofertas = Ofertas.objects.values('Cod_oferta', 'Puesto_oferta').filter(Estado = True).order_by( '-Estado' , '-Fecha_publicacion')
		lista_plazas = Aplicaciones.objects.filter(Cod_solicitud = codigo)
		solicitud = Solicitud.objects.get(codsolicitud=codigo)
	ctx = {
		'lista_ofertas':lista_ofertas,
		'lista_plazas':lista_plazas,
		'solicitud':solicitud,
	}

	return render(request, 'plazas_aplicado.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def ofertas_publicadas(request):

	lista_ofertas = Ofertas.objects.all()
	total = lista_ofertas.count()
	# page = request.GET.get('page', 1)
	# paginator = Paginator(lista_ofertas, 10)
	# try:
	# 	lista_ofertas = paginator.page(page)
	# except PageNotAnInteger:
	# 	lista_ofertas = paginator.page(1)
	# except EmptyPage:
	# 	lista_ofertas = paginator.page(paginator.num_pages)

	ctx={
		'lista_ofertas':lista_ofertas,
		'total':total
	}

	return render(request, 'ofertas_publicadas.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def candidatos_por_plazas(request, codigo):
	lista_aplicaciones = Aplicaciones.objects.filter(Cod_oferta = codigo)
	total = lista_aplicaciones.count()
	# page = request.GET.get('page', 1)
	# paginator = Paginator(lista_aplicaciones, 10)
	# try:
	# 	lista_aplicaciones = paginator.page(page)
	# except PageNotAnInteger:
	# 	lista_aplicaciones = paginator.page(1)
	# except EmptyPage:
	# 	lista_aplicaciones = paginator.page(paginator.num_pages)
	ctx = {
		'lista_aplicaciones':lista_aplicaciones,
		'total':total,
	}
	return render(request, 'candidatos_por_plazas.html', ctx)



@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def ofertas_activas(request):
	lista_ofertas = Ofertas.objects.filter(Estado = True)
	total = lista_ofertas.count()

	ctx ={
		'lista_ofertas':lista_ofertas,
		'total':total		
	}
	return render(request, 'ofertas_activas.html', ctx)

@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def ofertas_inactivas(request):
	lista_ofertas = Ofertas.objects.filter(Estado = False)
	total = lista_ofertas.count()

	ctx ={
		'lista_ofertas':lista_ofertas,
		'total':total		
	}
	return render(request, 'ofertas_inactivas.html', ctx)


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def ingresados_cc(request):

	list_cc = SeguimientoXAplicacion.objects.filter(CC = True)
	total = list_cc.count()
	ctx = {
		'list_cc':list_cc,
		'total':total
	}

	return render(request, 'ingresados_cc.html',ctx)


@login_required(login_url= "/administrador/login/")
@permission_required('admin.ver_admin')
def aplicaciones_hoy(request):
	import datetime
	fecha = datetime.date.today()
	lista_aplicaciones_hoy = Aplicaciones.objects.filter(Fecha = fecha)
	ctx = {
		'lista_aplicaciones_hoy':lista_aplicaciones_hoy,

	}

	return render(request, 'aplicaciones_hoy.html', ctx)

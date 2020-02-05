# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers  import make_password
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User , Group
from solicitud.models import *
from administrador.models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth.hashers import check_password
import base64
import uuid, json, pyodbc, os
from django.db import connection
from django.conf import settings
from django.core.files.base import ContentFile
from io import StringIO
from django.db.models import Q
from PIL import Image
import ldap

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


@transaction.atomic
def login_internas(request):
	logout(request)
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		if settings.EN_SERVIDOR == True:
			active_directory = auth(username, password)
			print active_directory
			if active_directory == True:

				if not User.objects.filter(username = username).exists():
					with transaction.atomic():
						try:
							user = User()
							user.is_superuser = False
							user.username = username
							user.is_staff = False
							user.set_password(password)
							user.save()
							g = Group.objects.get(id=2)
							g.user_set.add(user)

							perfil = Solicitud()
							perfil.cod_user = user
							perfil.vista = 1
							perfil.estado = 1
							perfil.correo = username
							perfil.save()
						except Exception as e:
							return render(request, 'login-interno.html')

					auth_login(request, user)
					return redirect('carga_foto')

				elif User.objects.get(username = username).last_login is not None:
					u = User.objects.get(username = username)
					u.set_password(password)
					u.save()
					usuario = authenticate(username = username, password = password)
					if usuario is not None:
						auth_login(request, usuario)
						return redirect('perfil')

				elif User.objects.get(username = username).last_login is None:
					u = User.objects.get(username = username)
					u.set_password(password)
					u.save()

					usuario = authenticate(username = username, password = password)
					
					if usuario is not None:
						auth_login(request, usuario)
						return redirect('carga_foto')
			else:
				
				error = 'Credenciales no validas'
				return render(request, 'login-interno.html', {'error': error})
		else:
			if not User.objects.filter(username = username).exists():
				with transaction.atomic():
					user = User()
					user.is_superuser = False
					user.username = username
					user.is_staff = False
					user.set_password(password)
					user.save()
					g = Group.objects.get(id=2)
					g.user_set.add(user)

					perfil = Solicitud()
					perfil.cod_user = user
					perfil.vista = 1
					perfil.estado = 1
					perfil.correo = username
					perfil.save()

				auth_login(request, user)
				return redirect('carga_foto')

			elif User.objects.get(username = username).last_login == None:
				usuario = authenticate(username = username, password = password)
				auth_login(request, usuario)
				return redirect('carga_foto')

			elif User.objects.get(username = username).last_login != None:
				usuario = authenticate(username = username, password = password)
				auth_login(request, usuario)
				return redirect('perfil')
			else:
				mensaje = 'error'
				return render(request, 'login-interno.html', {'mensaje': mensaje})

	return render(request, 'login-interno.html')


@permission_required('empleado.ver_internas')
@login_required()
@transaction.atomic
def carga_foto(request):
	if request.method == 'POST':
		with transaction.atomic():
			try:
				foto_usuario = request.FILES.get('foto_usuario')
				datos_imagen = request.POST.get('datos_imagen')
				nombre = request.POST.get('nombre')
				correo = request.POST.get('correo')
				apellido = request.POST.get('apellido')
				#Cortar imagen
				print datos_imagen
				try:
					if datos_imagen != '' and datos_imagen != None:
						print 'in if'
						image =  Image.open(foto_usuario)
						ancho, alto = image.size
						size = (int(ancho), int(alto))
						nueva_imagen = image.resize(size)
						region = (int(datos_imagen.split(",")[0]), int(datos_imagen.split(",")[1]), int(datos_imagen.split(",")[2]), int(datos_imagen.split(",")[3]))
						foto_perfil = nueva_imagen.crop(region)
						ruta_foto = 'foto_perfil_' + str(request.user.id) + '.jpg'
						foto_perfil.save(os.path.join(settings.MEDIA_ROOT, 'foto_perfil_' + str(request.user.id) + '.jpg'))
						Solicitud.objects.filter(cod_user=request.user.id).update(
							nombres = nombre,
							primerapellido = apellido,
							foto_usuario=ruta_foto,
							empleado= True,
							correo = correo
							)
						User.objects.filter(id=request.user.id).update(
							first_name = nombre,
							last_name = apellido,
							is_active = True,
							email = correo)
						return redirect('perfil')
					else:
						Solicitud.objects.filter(cod_user=request.user.id).update(
							nombres = nombre,
							primerapellido = apellido,
							empleado= True
							)
						User.objects.filter(id=request.user.id).update(
							first_name = nombre,
							last_name = apellido,
							is_active = True)
						return redirect('perfil')

				except Exception as e:
					return render(request, 'completar_perfil.html', {'error':'error', 'mensaje':e})
			except Exception as e:
				return render(request, 'completar_perfil.html', {'error':'error', 'mensaje':e})

	return render(request, 'completar_perfil.html')
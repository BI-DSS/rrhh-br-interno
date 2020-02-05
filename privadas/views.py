# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from models import *
from solicitud.models import *
from privadas.forms import *
from general.views import *
from forms import *
from django.template import RequestContext
from django.db import transaction, IntegrityError
import json
from django.http import HttpResponse


def ajax_departamento(request):
	if request.is_ajax():
  		codpais = request.GET['codpais']
  		data = list(Departamento.objects.values('coddepartamento', 'descripciondepartamento').filter(codpais = codpais))
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_municipio(request):
	if request.is_ajax():
  		coddepartamento = request.GET['coddepartamento']
  		data = list(Municipio.objects.values('codmunicipio', 'descripcionmunicipio').filter(coddepartamento = coddepartamento))
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_adicionarorg(request):
	if request.is_ajax():
  		nombre = request.GET['nombre']
		Grupo_organizacion.objects.create(nombre_organizacion=nombre)
		exito = 'exito'
		return HttpResponse(exito)

def ajax_cargarorgs(request):
	if request.is_ajax():
  		data = list(Grupo_organizacion.objects.values('cod_organizaciones', 'nombre_organizacion').all())
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_municipios_pais(request):
	if request.is_ajax():
  		codpais = request.GET['codpais']
  		data = list(Municipio.objects.values('codmunicipio', 'descripcionmunicipio').filter(coddepartamento__codpais__codpais = codpais))
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_universidades(request):
	if request.is_ajax():
  		data = list(Universidad.objects.values('cod_univesidad', 'nombre').all())
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_campus(request):
	if request.is_ajax():
  		id_universidad = request.GET['id_universidad']
  		data = list(Campus.objects.values('cod_campus', 'nombre').filter(cod_universidad = id_universidad))
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_carreras(request):
	if request.is_ajax():
  		id_universidad = request.GET['id_universidad']
  		data = list(Carrera.objects.values('cod_carreras', 'nombre_carrera').filter(cod_campus=id_universidad))
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_colegios(request):
	if request.is_ajax():
  		data = list(Colegio.objects.values('cod_colegios', 'nombre').all())
  		return HttpResponse(json.dumps(data), content_type='application/json')

def ajax_escuelas(request):
	if request.is_ajax():
  		data = list(Escuela.objects.values('cod_escuelas', 'nombre').all())
  		return HttpResponse(json.dumps(data), content_type='application/json')

PROFESION = {'Asalariado':'A', 'Independiente':'I', 'Jubilado':'J', 'Estudiante':'E', 'Ama de casa':'A', 'Otros':'O'}

def ajax_hermanos(request):
	if request.is_ajax():
		lista_hermanos = request.GET.getlist('lista_hermanos[]')
		cod_solicitud = request.GET.get('ingreso')
		solicitud = Solicitud.objects.get(codsolicitud=int(cod_solicitud))
		print lista_hermanos
		print cod_solicitud
		contador = 0
		for hermano in lista_hermanos:
			hermano_split = hermano.split("/")
			Hermano.objects.create(
				nombrecompleto=str(hermano_split[0]),
				edad=int(hermano_split[1]),
				domicilio=str(hermano_split[2]),
				telefono=str(hermano_split[3]),
				ocupacion=str(PROFESION[str(hermano_split[4])]),
				codsolicitud=solicitud)
			contador = contador + 1
		Solicitud.objects.filter(codsolicitud=int(cod_solicitud)).update(cantidadhermanos=contador)
		return HttpResponse(True)


@transaction.atomic
def form_soli_1(request, oferta):
	oferta = oferta
	form = SolicitudFrm()
	orga = Grupo_organizacion.objects.all()
	lista_seguros = Seguros.objects.all()
	lista_paises = Pais.objects.all()
	lista_departamentos = Departamento.objects.filter(codpais=1)
	lista_municipios = Municipio.objects.filter(coddepartamento__codpais__codpais=1)
	if request.POST:
		with transaction.atomic():
			try:
				pais_nacionalidad = Pais.objects.get(codpais=request.POST.get('nacionalidad'))
				ingreso = Solicitud()
				ingreso.anonima = True
				ingreso.nombres = None if request.POST.get('nombres') == '' else request.POST.get('nombres')
				ingreso.primerapellido = None if request.POST.get('primerapellido') == '' else request.POST.get('primerapellido')
				ingreso.segundoapellido = None if request.POST.get('segundoapellido') == '' else request.POST.get('segundoapellido')
				ingreso.sexo = None if request.POST.get('sexo') == '' else request.POST.get('sexo')
				ingreso.estadocivil = None if request.POST.get('estadocivil') == '' else request.POST.get('estadocivil')
				ingreso.apellidocasada = None if request.POST.get('apellidocasada') == '' else request.POST.get('apellidocasada')
				ingreso.direcciondomicilio = None if request.POST.get('direcciondomicilio') == '' else request.POST.get('direcciondomicilio')
				ingreso.coddepartamentodomicilio = Departamento.objects.get(pk=request.POST.get('coddepartamentodomicilio'))
				ingreso.codmunicipiodomicilio = Municipio.objects.get(pk=request.POST.get('codmunicipiodomicilio'))
				ingreso.telefonofijo = None if request.POST.get('telefonofijo') == '' else request.POST.get('telefonofijo')
				ingreso.celular = None if request.POST.get('celular') == '' else request.POST.get('celular')
				ingreso.lugarnacimiento = pais_nacionalidad.descripcionpais
				ingreso.codpaisnacimiento = Pais.objects.get(codpais=request.POST.get('nacionalidad'))
				ingreso.fechanacimiento = None if request.POST.get('fechanacimiento') == '' else request.POST.get('fechanacimiento')
				ingreso.edad = None if request.POST.get('edad') == '' else request.POST.get('edad')
				ingreso.profesion = None if request.POST.get('profesion') == '' else request.POST.get('profesion')
				ingreso.identidad = None if request.POST.get('identidad') == '' else request.POST.get('identidad')
				ingreso.codmunicipioidentidad = Municipio.objects.get(pk=request.POST.get('codmunicipioidentidad'))
				ingreso.automovil = None if request.POST.get('automovil') == '' else request.POST.get('automovil')
				ingreso.licencia = None if request.POST.get('licencia') == '' else request.POST.get('licencia')
				ingreso.liviana = None if request.POST.get('liviana') == '' else request.POST.get('liviana')
				ingreso.pesada = None if request.POST.get('pesada') == '' else request.POST.get('pesada')
				ingreso.motocicleta = None if request.POST.get('motocicleta') == '' else request.POST.get('motocicleta')
				ingreso.polizaseguro = None if request.POST.get('polizaseguro') == '' else request.POST.get('polizaseguro')
				ingreso.cod_seguros = None if request.POST.get('compania') == '' else Seguros.objects.get(cod_seguros=request.POST.get('compania'))
				ingreso.companiapoliza =None if request.POST.get('compania') == '' else Seguros.objects.get(cod_seguros=request.POST.get('compania')).compania_seguros
				ingreso.tipodeporte = None if request.POST.get('tipodeporte') == '' else request.POST.get('tipodeporte')
				ingreso.deporte = None if request.POST.get('deporte') == '' else request.POST.get('deporte')
				ingreso.fechadeporte = None if request.POST.get('fechadeporte') == '' else request.POST.get('fechadeporte')
				ingreso.numeroihss = None if request.POST.get('numeroihss') == '' else request.POST.get('numeroihss')
				ingreso.rtn = None if request.POST.get('rtn') == '' else request.POST.get('rtn')
				ingreso.numeropasaporte = None if request.POST.get('numeropasaporte') == '' else request.POST.get('numeropasaporte')
				ingreso.correo = request.POST.get('correo')
				ingreso.estado = 0 
				ingreso.vista = 2
				ingreso.save()
				organizaciones_lista = request.POST.get('input_registros')
				if  organizaciones_lista != '':
					organizaciones_temp = organizaciones_lista.split("_")
					for org_temp in organizaciones_temp:
						if org_temp != '':
							values_org = org_temp.split("/")
							Organizacion.objects.create(
								cod_grupo_organizacion=values_org[0],
								nombre=values_org[1],
								cod_solicitud=ingreso.codsolicitud)
				return redirect(reverse('form_soli_2', kwargs={'oferta': oferta, 'codigo': ingreso.codsolicitud}))
			except Exception as e:
				raise
			
	ctx ={
		'form': form ,
		 'orga': orga ,
		 'lista_departamentos':lista_departamentos ,
		 'lista_municipios':lista_municipios,
		 'lista_paises':lista_paises,
		 'lista_seguros':lista_seguros,
		 'oferta':oferta
	}
	return render(request, 'form_1.html', ctx)


@transaction.atomic
def form_soli_2(request, oferta, codigo):
	oferta = oferta
	ingreso = Solicitud.objects.get(pk=codigo)
	form = SolicitudFrm()
	herm = HermanoFrm()
	hijo = HijoFrm()
	depen = DependienteFrm()
	if request.POST:
		with transaction.atomic():
			try:
				nombrecompleto = request.POST.getlist('nombrecompleto[]')
				edad = request.POST.getlist('edad[]')
				domicilio = request.POST.getlist('domicilio[]')
				telefono = request.POST.getlist('telefono[]')
				ocupacion = request.POST.getlist('ocupacion[]')

				counter = 0
				for y in nombrecompleto:
					if y != '' and y != None:
						hermano = Hermano()
						hermano.codsolicitud = Solicitud.objects.get(pk=codigo)
						hermano.nombrecompleto = None if nombrecompleto[counter] == '' else nombrecompleto[counter]
						hermano.edad = None if edad[counter] == '' else edad[counter]
						hermano.domicilio = None if domicilio[counter] == '' else domicilio[counter]
						hermano.telefono = None if telefono[counter] == '' else telefono[counter]
						hermano.ocupacion = None if ocupacion[counter] == '' else ocupacion[counter]
						hermano.save()
						counter += 1

				nombreshijo = request.POST.getlist('nombreshijo[]')
				apellidoshijo = request.POST.getlist('apellidoshijo[]')
				edadhijo = request.POST.getlist('edadhijo[]')

				contadorhijo = 0
				
				for h in nombreshijo:
					if h != '' and h != None:
						hijo =Hijo()
						hijo.codsolicitud = Solicitud.objects.get(pk=codigo)
						hijo.nombreshijo = None if nombreshijo[contadorhijo] == '' else nombreshijo[contadorhijo]
						hijo.apellidoshijo = None if apellidoshijo[contadorhijo] == '' else apellidoshijo[contadorhijo]
						hijo.edadhijo = None if edadhijo[contadorhijo] == '' else edadhijo[contadorhijo]
						hijo.save()
						contadorhijo += 1


				nombredependiente = request.POST.getlist('nombredependiente[]')
				tipodependencia = request.POST.getlist('tipodependencia[]')

				contadordepen = 0
				for d in nombredependiente:
					if d != '' and d != None:
						dependiente = Dependiente()
						dependiente.codsolicitud = Solicitud.objects.get(pk=codigo)
						dependiente.nombredependiente = None if nombredependiente[contadordepen] == '' else nombredependiente[contadordepen]
						dependiente.tipodependencia = None if tipodependencia[contadordepen] == '' else tipodependencia[contadordepen]
						dependiente.save()
						contadordepen += 1

				ingreso = Solicitud.objects.get(codsolicitud=codigo)
				ingreso.nombrespadre = None if request.POST.get('nombrespadre') == '' else request.POST.get('nombrespadre')
				ingreso.apellidospadre = None if request.POST.get('apellidospadre') == '' else request.POST.get('apellidospadre')
				ingreso.edadpadre = None if request.POST.get('edadpadre') == '' else request.POST.get('edadpadre')
				ingreso.domiciliopadre = None if request.POST.get('domiciliopadre') == '' else request.POST.get('domiciliopadre')
				ingreso.telefonopadre = None if request.POST.get('telefonopadre') == '' else request.POST.get('telefonopadre')
				ingreso.profesionpadre = None if request.POST.get('profesionpadre') == '' else request.POST.get('profesionpadre')
				ingreso.celularpadre = None if request.POST.get('celularpadre') == '' else request.POST.get('celularpadre')
				ingreso.direccionlaboralpadre = None if request.POST.get('direccionlaboralpadre') == '' else request.POST.get('direccionlaboralpadre')
				ingreso.nombresmadre = None if request.POST.get('nombresmadre') == '' else request.POST.get('nombresmadre')
				ingreso.apellidosmadre = None if request.POST.get('apellidosmadre') == '' else request.POST.get('apellidosmadre')
				ingreso.edadmadre =None if request.POST.get('edadmadre') == '' else request.POST.get('edadmadre')
				ingreso.domiciliomadre = None if request.POST.get('domiciliomadre') == '' else request.POST.get('domiciliomadre')
				ingreso.telefonomadre = None if request.POST.get('telefonomadre') == '' else request.POST.get('telefonomadre')
				ingreso.celularmadre = None if request.POST.get('celularmadre') == '' else request.POST.get('celularmadre')
				ingreso.profesionmadre = None if request.POST.get('profesionmadre') == '' else request.POST.get('profesionmadre')
				ingreso.direccionlaboralmadre = None if request.POST.get('direccionlaboralmadre') == '' else request.POST.get('direccionlaboralmadre')
				ingreso.hermanos = None if request.POST.get('hermanos') == '' else request.POST.get('hermanos')
				ingreso.cantidadhermanos = counter
				ingreso.nombreconyugue = None if request.POST.get('nombreconyugue') == '' else request.POST.get('nombreconyugue')
				ingreso.edadconyugue = None if request.POST.get('edadconyugue') == '' else request.POST.get('edadconyugue')
				ingreso.domicilioconyugue = None if request.POST.get('domicilioconyugue') == '' else request.POST.get('domicilioconyugue')
				ingreso.telefonoconyugue = None if request.POST.get('telefonoconyugue') == '' else request.POST.get('telefonoconyugue')

				ingreso.profesionconyugue = None if request.POST.get('profesionconyugue') == '' else request.POST.get('profesionconyugue')
				ingreso.direccionlaboralconyugue = None if request.POST.get('direccionlaboralconyugue') == '' else request.POST.get('direccionlaboralconyugue')
				ingreso.vista = 3
				ingreso.save()
				return redirect(reverse('form_soli_3', kwargs={'oferta':oferta ,'codigo': ingreso.codsolicitud}))

			except Exception as e:
				raise e
				mensaje = 'error'
	ctx = {
		'form': form,
		'herm':herm,
		'hijo':hijo,
	    'ingreso': ingreso,
	    'depen':depen,
	   	'oferta':oferta

	}

	return render(request, 'form_2.html', ctx )

@transaction.atomic
def form_soli_3(request, oferta, codigo):
	oferta= oferta
	ingreso = Solicitud.objects.get(pk=codigo)
	form = SolicitudFrm()
	cuenta = CuentaFrm()
	if request.POST:
		with transaction.atomic():
			try:
				tipo_cuenta = request.POST.getlist('tipo_cuenta[]')
				cantidad = request.POST.getlist('cantidad[]')
				institucion = request.POST.getlist('institucion[]')
				numero_cuenta = request.POST.getlist('numero_cuenta[]')

				contcuentas = 0
				for x in tipo_cuenta:
					cuenta = Cuenta()
					cuenta.cod_solicitud = Solicitud.objects.get(pk=codigo)
					cuenta.tipo_cuenta = None if tipo_cuenta[contcuentas] == '' else tipo_cuenta[contcuentas]
					cuenta.cantidad = None if cantidad[contcuentas] == '' else cantidad[contcuentas]
					cuenta.institucion = None if institucion[contcuentas] == '' else institucion[contcuentas]
					cuenta.numero_cuenta = None if numero_cuenta[contcuentas] == '' else numero_cuenta[contcuentas]
					cuenta.save()
					contcuentas += 1



				ingreso = Solicitud.objects.get(codsolicitud=codigo)
				ingreso.tipovivienda = None if request.POST.get('tipovivienda') == '' else request.POST.get('tipovivienda')
				ingreso.totalamortizacion = None if request.POST.get('totalamortizacion') == '' else request.POST.get('totalamortizacion')
				ingreso.totalinquilino = None if request.POST.get('totalinquilino') == '' else request.POST.get('totalinquilino')
				ingreso.totalpensionista = None if request.POST.get('totalpensionista') == '' else request.POST.get('totalpensionista')
				ingreso.deudas  = None if request.POST.get('deudas') == '' else request.POST.get('deudas')
				ingreso.nombreacreedor = None if request.POST.get('nombreacreedor') == '' else request.POST.get('nombreacreedor')
				ingreso.montodeuda = None if request.POST.get('montodeuda') == '' else request.POST.get('montodeuda')
				ingreso.cuotamensual = None if request.POST.get('cuotamensual') == '' else request.POST.get('cuotamensual')
				ingreso.embargado = None if request.POST.get('embargado') == '' else request.POST.get('embargado')
				ingreso.nombrequienembargo = None if request.POST.get('nombrequienembargo') == '' else request.POST.get('nombrequienembargo')
				ingreso.motivoembargo = None if request.POST.get('motivoembargo') == '' else request.POST.get('motivoembargo')
				ingreso.montoembargo = None if request.POST.get('montoembargo') == '' else request.POST.get('montoembargo')

				ingreso.valoresefectivo = None if request.POST.get('valoresefectivo') == '' else request.POST.get('valoresefectivo')
				ingreso.montoefectivo = None if request.POST.get('montoefectivo') == '' else request.POST.get('montoefectivo')
				ingreso.familiaresinstitucion = None if request.POST.get('familiaresinstitucion') == '' else request.POST.get('familiaresinstitucion')
				ingreso.nombrefamiliar = None if request.POST.get('nombrefamiliar') == '' else request.POST.get('nombrefamiliar')
				ingreso.parentesco = None if request.POST.get('parentesco') == '' else request.POST.get('parentesco')
				ingreso.puestofamiliar = None if request.POST.get('puestofamiliar') == '' else request.POST.get('puestofamiliar')
				ingreso.trabajarcualquierlugar = None if request.POST.get('trabajarcualquierlugar') == '' else request.POST.get('trabajarcualquierlugar')
				ingreso.nombrequienrecomienda = None if request.POST.get('nombrequienrecomienda') == '' else request.POST.get('nombrequienrecomienda')
				ingreso.puestoquesolicita = None if request.POST.get('puestoquesolicita') == '' else request.POST.get('puestoquesolicita')
				ingreso.sueldopretende = None if request.POST.get('sueldopretende') == '' else request.POST.get('sueldopretende')
				ingreso.fechainicio = None if request.POST.get('fechainicio') == '' else request.POST.get('fechainicio')
				ingreso.vista = 4
				ingreso.save()

				return redirect(reverse('form_soli_4', kwargs={'oferta':oferta, 'codigo': ingreso.codsolicitud}))

			except Exception as e:
				raise e
				mensaje = 'error'

	ctx = {
		'form': form,
		'ingreso': ingreso,
		'cuenta': cuenta,
		'oferta': oferta
	}


	return render(request, 'form_3.html', ctx )

@transaction.atomic
def form_soli_4(request, oferta, codigo):
	oferta= oferta
	ingreso = Solicitud.objects.get(pk=codigo)
	histo = HistoriallaboralFrm()
	form = SolicitudFrm()
	if request.POST:
		with transaction.atomic():
			try:
				nombreempresa = request.POST.getlist('nombreempresa[]')
				fechaingreso = request.POST.getlist('fechaingreso[]')
				fechaegreso = request.POST.getlist('fechaegreso[]')
				direccionempresa = request.POST.getlist('direccionempresa[]')
				nombrejefeinmediato = request.POST.getlist('nombrejefeinmediato[]')
				motivoretiro = request.POST.getlist('motivoretiro[]')
				counter = 0
				for x in nombreempresa:
					laboral = Historiallaboral()
					laboral.codsolicitud = Solicitud.objects.get(pk=codigo)
					laboral.nombreempresa = None if nombreempresa[counter] == '' else nombreempresa[counter]
					laboral.fechaingreso = None if fechaingreso[counter] == '' else fechaingreso[counter]
					laboral.fechaegreso = None if fechaegreso[counter] == '' else fechaegreso[counter]
					laboral.direccionempresa = None if direccionempresa[counter] == '' else direccionempresa[counter]
					laboral.nombrejefeinmediato = None if nombrejefeinmediato[counter] == '' else nombrejefeinmediato[counter]
					laboral.motivoretiro = None if motivoretiro[counter] == '' else motivoretiro[counter]
					ingreso.vista = 5
					ingreso.save()
					laboral.save()
					counter += 1
				return redirect(reverse('form_soli_5', kwargs={'oferta':oferta, 'codigo': ingreso.codsolicitud }))
				
			except Exception as e:
				raise
			
	ctx = {
		'histo': histo,
		'ingreso': ingreso,
		'oferta':oferta
	}
	return render(request, 'form_4.html', ctx )


COMPETENCIAS = {'1':'TRABAJO EN EQUIPO', '2':'PUNTUALIDAD', '3':'LIDERAZGO', '4':'INNOVACION', '5':'CREATIVIDAD', '6':'INICIATIVA'}
@transaction.atomic
def form_soli_5(request, oferta, codigo):
	oferta= oferta
	ingreso = Solicitud.objects.get(pk=codigo)
	idioma = IdiomaFrm()
	form = SolicitudFrm()
	formHisAca = HistorialacademicoFrm()
	formcurso = CursoFrm()
	formhabilidad = HabilidadFrm()
	lista_departamentos = Departamento.objects.filter(codpais=1)
	if request.POST:
		with transaction.atomic():
			try:
				idiomas = request.POST.get('idiomas')
				estudios = request.POST.get('estudios')
				cursos = request.POST.get('cursos')
				habilidades = request.POST.get('habilidades')
				competencias = request.POST.get('competencias')
				if idiomas != '':
					lista_idiomas = idiomas.split("_")
					for	idioma in lista_idiomas:
						if idioma != '':
							datos_idioma = idioma.split("/")
							Idioma.objects.create(
								nombre=datos_idioma[0],
								habla=int(datos_idioma[1].strip(" %")),
								escritura=int(datos_idioma[2].strip(" %")),
								lectura=int(datos_idioma[1].strip(" %")),
								cod_solicitud=ingreso)
				if estudios != '':
					lista_estudios =  estudios.split("_")
					for	estudio in lista_estudios:
						if estudio != '':
							datos_estudio = estudio.split("/")
							Historialacademico.objects.create(
								nombreinstitucion=datos_estudio[0],
								nivelestudios=datos_estudio[1],
								lugarestudio=datos_estudio[2],
								tituloobtenido=datos_estudio[3],
								inicio=int(datos_estudio[4]),
								fin=int(datos_estudio[5]),
								codsolicitud=ingreso)
				if	cursos != '':
					lista_cursos = cursos.split("_")
					for	curso in lista_cursos:
						if	curso != '':
							datos_curso = curso.split("/")
							Curso.objects.create(
								temacurso=datos_curso[0],
								nombrecentroestudio=datos_curso[1],
								direccioncentroestudio=datos_curso[2],
								duracion=datos_curso[3],
								titulo=datos_curso[4],
								codsolicitud=ingreso)
				if	habilidades != '':
					lista_habilidades = habilidades.split("_")
					for	habilidad in lista_habilidades:
						if	habilidad != '':
							datos_habilidad = habilidad.split("/")
							Habilidad.objects.create(
								nombre_habilidad=datos_habilidad[0],
								porcentaje=int(datos_habilidad[1].strip(" %")),
								cod_solicitud=ingreso)
				if competencias != '':
					lista_competencias = competencias.split("/")
					for competencia in lista_competencias:
						if	competencia != '':
							Competencia.objects.create(
								nombre_competencia=COMPETENCIAS[competencia],
								posee=True,
								cod_solicitud=ingreso)
				ingreso.vista = 6
				ingreso.save()
				return redirect(reverse('form_soli_6', kwargs={'oferta':oferta, 'codigo': ingreso.codsolicitud }))

			except Exception as e:
				raise e
				mensaje = 'error'

	ctx = {
		'lista_departamentos':lista_departamentos,
		'idioma': idioma,
		'form': form,
		'formcurso':formcurso,
		'formhistoaca': formHisAca,
		'formhabilidad':formhabilidad,
		'oferta':oferta,
		'ingreso':ingreso
	}
	return render(request, 'form_5.html', ctx )


@transaction.atomic
def form_soli_6(request, oferta, codigo):
	oferta = oferta
	solicitud = Solicitud.objects.get(codsolicitud=codigo)
	preguntas = Preguntas.objects.filter(Cod_oferta = oferta)
	form = ReferenciaFrm()
	formRefPer = ReferenciaPersonalFrm()
	if request.POST:
		with transaction.atomic():
			#try:
			preguntas =Preguntas.objects.filter(Cod_oferta = oferta).values_list('Cod_pregunta', flat= True)
			nombrecompleto = request.POST.getlist('nombrecompleto[]')
			profesion = request.POST.getlist('profesion[]')
			direccion = request.POST.getlist('direccion[]')
			telefono = request.POST.getlist('telefono[]')
			counter_lab = 0
			for x in nombrecompleto:
				referencia = Referencia()
				referencia.codsolicitud = Solicitud.objects.get(pk=codigo)
				referencia.nombrecompleto = None if nombrecompleto[counter_lab] == '' else nombrecompleto[counter_lab]
				referencia.profesion = None if profesion[counter_lab] == '' else profesion[counter_lab]
				referencia.direccion = None if direccion[counter_lab] == '' else direccion[counter_lab]
				referencia.telefono = None if telefono[counter_lab] == '' else telefono[counter_lab]
				referencia.save()
				counter_lab += 1

			counter_per = 0
			nombre_personal = request.POST.getlist('nombre_personal[]')
			profesion_personal = request.POST.getlist('profesion_personal[]')
			direccion_personal = request.POST.getlist('direccion_personal[]')
			telefono_personal = request.POST.getlist('telefono_personal[]')
			for x in nombre_personal:
				referencia = Referenciaspersonal()
				referencia.codsolicitud = Solicitud.objects.get(pk=codigo)
				referencia.nombre_personal = None if nombre_personal[counter_per] == '' else nombre_personal[counter_per]
				referencia.profesion_personal = None if profesion_personal[counter_per] == '' else profesion_personal[counter_per]
				referencia.direccion_personal = None if direccion_personal[counter_per] == '' else direccion_personal[counter_per]
				referencia.telefono_personal = None if telefono_personal[counter_per] == '' else telefono_personal[counter_per]
				referencia.save()
				counter_per += 1

			try:
				archivo = request.FILES['cv']
				print archivo
				solicitud.cv = archivo
				hola= archivo.name
				print hola
				solicitud.cvnombre = hola
				
			except Exception as e:
				raise
		
			solicitud.vista = 7
			solicitud.estado = 1
			solicitud.save()


			aplicacion = Aplicaciones()
			aplicacion.Cod_oferta = Ofertas.objects.get(Cod_oferta = oferta)
			aplicacion.Cod_solicitud = Solicitud.objects.get(codsolicitud = codigo)
			aplicacion.save()

			return redirect('gracias')

	ctx = {
		'form': form,
		'formRefPer': formRefPer,
		'solicitud': solicitud,
		'oferta': oferta,
		'preguntas':preguntas
	}
	return render(request, 'form_6.html', ctx)


def gracias(request):

	return render(request, 'mensaje-gracias.html')


def historial_laboral(request ,oferta , codigo):
	Solicitud.objects.filter(codsolicitud=codigo).update(
		vista = 5
		)
	return redirect(reverse('form_soli_5', kwargs={'oferta':oferta, 'codigo':codigo }))






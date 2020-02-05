from django.conf.urls import url
from solicitud import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^ajax_departamento/$', views.ajax_departamento, name='ajax_departamento'),
	url(r'^ajax_municipio/$', views.ajax_municipio, name='ajax_municipio'),
	url(r'^ajax_municipios_pais/$', views.ajax_municipios_pais, name='ajax_municipios_pais'),
	url(r'^ajax_hermanos/$', views.ajax_hermanos, name='ajax_hermanos'),
	url(r'^ajax_cargarorgs/$', views.ajax_cargarorgs, name='ajax_cargarorgs'),
	url(r'^ajax_adicionarorg/$', views.ajax_adicionarorg, name='ajax_adicionarorg'),
	url(r'^ajax_escuelas/$', views.ajax_escuelas, name='ajax_escuelas'),
	url(r'^ajax_colegios/$', views.ajax_colegios, name='ajax_colegios'),
	url(r'^ajax_universidades/$', views.ajax_universidades, name='ajax_universidades'),
	url(r'^ajax_campus/$', views.ajax_campus, name='ajax_campus'),
	url(r'^ajax_carreras/$', views.ajax_carreras, name='ajax_carreras'),
	url(r'^solicitud_1/(?P<codigo>\d+)$', views.solicitud_1, name='solicitud_1'),
	url(r'^solicitud_2/(?P<codigo>\d+)$', views.solicitud_2, name='solicitud_2'),
	url(r'^solicitud_3/(?P<codigo>\d+)$', views.solicitud_3, name='solicitud_3'),
	url(r'^solicitud_4/(?P<codigo>\d+)$', views.solicitud_4, name='solicitud_4'),
	url(r'^no_historial_laboral/$', views.no_historial_laboral, name='no_historial_laboral'),
	url(r'^solicitud_5/(?P<codigo>\d+)$', views.solicitud_5, name='solicitud_5'),
	url(r'^solicitud_6/(?P<codigo>\d+)$', views.solicitud_6, name='solicitud_6'),
]
from django.conf.urls import url
from privadas import views
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
	url(r'^form_soli_1/(?P<oferta>\d+)$', views.form_soli_1, name='form_soli_1'),
	url(r'^form_soli_2/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.form_soli_2, name='form_soli_2'),
	url(r'^form_soli_3/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.form_soli_3, name='form_soli_3'),
	url(r'^form_soli_4/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.form_soli_4, name='form_soli_4'),
	url(r'^historial_laboral/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.historial_laboral, name='historial_laboral'),
	url(r'^form_soli_5/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.form_soli_5, name='form_soli_5'),
	url(r'^form_soli_6/(?P<oferta>\d+)/(?P<codigo>\d+)$', views.form_soli_6, name='form_soli_6'),
	url(r'^gracias/$', views.gracias, name='gracias'),
]
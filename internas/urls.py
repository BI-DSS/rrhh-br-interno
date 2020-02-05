from django.conf.urls import url
from internas import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.login_internas, name='login_internas'),
	url(r'^completar_perfil/$', views.carga_foto, name='carga_foto'),

]
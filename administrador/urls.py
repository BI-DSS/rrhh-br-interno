from django.conf.urls import url
from administrador.views import *

urlpatterns = [
    url(r'^login/$', login_admin, name='login_admin'),
    url(r'^logoutadmin/$', logout_admin, name='logout_admin'),
    url(r'^inicio/$', lista_candidatos, name='lista_candidatos'),
    url(r'^usuarios-registrados/$', lista_registrados, name='lista_registrados'),
    url(r'^perfilcandidato/(?P<solicitud>\d+)/$', perfil_candidato, name='perfil_candidato'),
    url(r'^informacioncandidato/(?P<solicitud>\d+)/$', informacion_candidato, name='informacion_candidato'),
    url(r'^familiacandidato/(?P<solicitud>\d+)/$', familia_candidato, name='familia_candidato'),
    url(r'^economiacandidato/(?P<solicitud>\d+)/$', economia_candidato, name='economia_candidato'),
    url(r'^trabajocandidato/(?P<solicitud>\d+)/$', trabajo_candidato, name='trabajo_candidato'),
    url(r'^estudioscandidato/(?P<solicitud>\d+)/$', estudios_candidato, name='estudios_candidato'),
    url(r'^referenciascandidato/(?P<solicitud>\d+)/$', referencias_candidato, name='referencias_candidato'),
    url(r'^listausuarios/$', lista_usuarios, name='lista_usuarios'),
    url(r'^usuario-nuevo/$', usuario_nuevo, name='usuario_nuevo'),
    url(r'^inhabilitar-usuario(?P<codigo>.+)/$', inhabilitar_usuario, name='inhabilitar_usuario'),
    url(r'^habilitar-usuario(?P<codigo>.+)/$', habilitar_usuario, name='habilitar_usuario'),
    
    ##################### OFERTAS LABORALES ##################################################
    url(r'^listaofertas/$', lista_ofertas, name='lista_ofertas'),
    url(r'^ofertanueva/$', oferta_nueva, name='oferta_nueva'),
    url(r'^update-oferta/(?P<codigo>\d+)/$', update_oferta, name='update_oferta'),
    url(r'^inhabilitar-oferta(?P<codigo>\d+)/$', inhabilitar_oferta, name='inhabilitar_oferta'),
    url(r'^habilitar-oferta(?P<codigo>\d+)/$', habilitar_oferta, name='habilitar_oferta'),
 
    url(r'^imprimir-solicitud-empleo/(?P<solicitud>\d+)/(?P<aplicacion>\d+)/$', GeneratePdf.as_view(), name='imprimircv'),

    ########################### Cantidatos por aferta####################################
    url(r'^cantidatos-por-plaza/(?P<codigo>\d+)/$', candidatos_plaza, name='candidatos_plaza'),
    url(r'^favorito/$', favorito, name='favorito'),
    url(r'^lista-favoritos/(?P<codigo>\d+)/$', lista_favoritos, name='lista_favoritos'),
    url(r'^visto/(?P<codigo>\d+)/$', visto, name='visto'),
    url(r'^dislike/(?P<codigo>\d+)/$', dislike, name='dislike'),
    url(r'^solicitud-admin/$', solicitud_admin, name='solicitud_admin'),
    url(r'^respuestas/$', respuestas, name='respuestas'),
    
#################################SEGUIMIENTO#################################
    url(r'^seguimiento/(?P<codigo>\d+)/$', seguimiento, name='seguimiento'),
    url(r'^Primera-entrevista/(?P<codigo>\d+)/$', Primera_entrevista, name='Primera_entrevista'),
    url(r'^Examen-psico/(?P<codigo>\d+)/$', Examen_psico, name='Examen_psico'),
    url(r'^Jefe-Inme/(?P<codigo>\d+)/$', Entrevista_jefe, name='Entrevista_jefe'),
    url(r'^Poligrafo/(?P<codigo>\d+)/$', Poligrafo, name='Poligrafo'),
    url(r'^socio/(?P<codigo>\d+)/$', socio, name='socio'),
    url(r'^Doc/(?P<codigo>\d+)/$', Doc, name='Doc'),
    url(r'^Medicos/(?P<codigo>\d+)/$', Medicos, name='Medicos'),
    url(r'^CC/(?P<codigo>\d+)/$', CC, name='CC'),
    url(r'^mensaje_gracias/(?P<codigo>\d+)/$', mensaje_gracias, name='mensaje_gracias'),

######################################CITAS #################################
    url(r'^Citas/$', Citas, name='Citas'),
    url(r'^PDFCitas/$', PDFCitas, name='PDFCitas'),
 
################################### CAMBIOS DEL 2018/03/07 ########################
    url(r'^plazas-aplicado/(?P<codigo>\d+)/$', plazas_aplicado, name='plazas_aplicado'),
    url(r'^ofertas-publicadas/$', ofertas_publicadas, name='ofertas_publicadas'),
    url(r'^candidatos-por-plazas/(?P<codigo>\d+)/$', candidatos_por_plazas, name='candidatos_por_plazas'),
    url(r'^ofertas-activas/$', ofertas_activas, name='ofertas_activas'),
    url(r'^ofertas-inactivas/$', ofertas_inactivas, name='ofertas_inactivas'),
    url(r'^ingresados-CC/$', ingresados_cc, name='ingresados_cc'),
    url(r'^aplicaciones-hoy/$', aplicaciones_hoy, name='aplicaciones_hoy'),
    #url(r'^areas/$', areas, name='areas'),
]



"""sf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('general.urls')),
    url(r'^solicitud-empleo/', include('solicitud.urls')),
    url(r'^administrador/', include('administrador.urls')),
    url(r'^promocion-interna/', include('internas.urls')),
    url(r'^vacantes/', include('privadas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = administrador.error_404
# handler500 = administrador.error_500


# def error_404(request):
#         data = {}
#         return render(request,'administrador/error_404.html', data)
 
# def error_500(request):
#         data = {}
#         return render(request,'administrador/error_500.html', data)
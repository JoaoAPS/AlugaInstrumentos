from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registration/', include('users.urls')),
    path('api/categorias/', include('categorias.urls')),
    path('api/equipamentos/', include('equipamentos.urls')),
    path('api/pedidos/', include('pedidos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

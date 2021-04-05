from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categorias/', include('categorias.urls')),
    path('api/equipamentos/', include('equipamentos.urls')),
    path('api/pedidos/', include('pedidos.urls')),
]

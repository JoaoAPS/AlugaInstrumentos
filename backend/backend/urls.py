from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth-token/', obtain_auth_token),
    path('api/categorias/', include('categorias.urls')),
    path('api/equipamentos/', include('equipamentos.urls')),
    path('api/pedidos/', include('pedidos.urls')),
]

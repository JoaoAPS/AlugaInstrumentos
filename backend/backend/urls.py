from django.contrib import admin
from django.urls import path, include

from users.views import AuthTokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', AuthTokenView.as_view(), name='auth-token'),
    path('api/categorias/', include('categorias.urls')),
    path('api/equipamentos/', include('equipamentos.urls')),
    path('api/pedidos/', include('pedidos.urls')),
]

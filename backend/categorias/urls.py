from rest_framework import routers

from categorias.views import CategoriaViewSet


router = routers.DefaultRouter()
router.register('', CategoriaViewSet)

urlpatterns = router.urls

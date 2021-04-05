from rest_framework import routers

from equipamentos.views import EquipamentoViewSet


router = routers.DefaultRouter()
router.register('', EquipamentoViewSet)

urlpatterns = router.urls

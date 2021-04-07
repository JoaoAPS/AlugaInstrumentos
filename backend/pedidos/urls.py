from rest_framework.routers import DefaultRouter, Route

from pedidos.views import PedidoViewset


router = DefaultRouter()
router.register('', PedidoViewset, basename='pedido')
router.routes.insert(0, Route(
    url=r'^{prefix}/{lookup}/$',
    mapping={
        'post': 'add_item',
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy',
    },
    name='{basename}-add_item',
    detail=True,
    initkwargs={'suffix': 'Detail'}
))

urlpatterns = router.urls

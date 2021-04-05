from django.contrib import admin

from equipamentos.models import Equipamento
from categorias.models import Categoria
from pedidos.models import Pedido
from reservas.models import Reserva
from users.models import User

admin.site.register(User)
admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(Categoria)
admin.site.register(Equipamento)

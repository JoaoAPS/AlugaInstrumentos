from rest_framework import serializers

from pedidos.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer do model Pedido"""

    class Meta:
        model = Pedido
        fields = ['user', 'equipamentos', 'start_date', 'end_date']
        depth = 1


class PedidoUpdateSerializer(serializers.ModelSerializer):
    """Serializer do model Pedido para requests de update"""

    class Meta:
        model = Pedido
        fields = ['start_date', 'end_date']

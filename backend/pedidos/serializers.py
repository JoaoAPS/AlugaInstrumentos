from rest_framework import serializers

from pedidos.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer do model Pedido"""

    class Meta:
        model = Pedido
        fields = ['id', 'user', 'equipamentos', 'start_date', 'end_date']
        depth = 1


class PedidoCreateSerializer(serializers.ModelSerializer):
    """Serializer do model Pedido para requests de create"""

    class Meta:
        model = Pedido
        fields = ['id', 'equipamentos', 'start_date', 'end_date']

    def validate(self, data):
        """Checa que end_date ocorre depois de start_date"""
        validate_dates(data)
        return data


class PedidoUpdateSerializer(serializers.ModelSerializer):
    """Serializer do model Pedido para requests de update"""

    class Meta:
        model = Pedido
        fields = ['start_date', 'end_date']

    def validate(self, data):
        """Checa que end_date ocorre depois de start_date"""
        print(data)
        validate_dates(data)
        return data


def validate_dates(data):
    """Checa que end_date ocorre depois de start_date"""
    if 'start_date' not in data.keys() or 'end_date' not in data.keys():
        return

    if data['start_date'] >= data['end_date']:
        raise serializers.ValidationError(
            "A data de término do aluguel deve ocorrer depois da data " +
            "de início!")

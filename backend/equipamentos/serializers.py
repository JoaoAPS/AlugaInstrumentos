from rest_framework import serializers

from equipamentos.models import Equipamento


class EquipamentoSerializer(serializers.ModelSerializer):
    """Serializer do model Equipamento"""

    class Meta:
        model = Equipamento
        fields = '__all__'

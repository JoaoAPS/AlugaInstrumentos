from rest_framework import serializers

from categorias.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Categoria"""

    class Meta():
        model = Categoria
        fields = ('id', 'name', 'is_instrument')

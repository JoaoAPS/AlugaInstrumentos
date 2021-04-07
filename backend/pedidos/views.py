from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from pedidos.models import Pedido
from pedidos import serializers
from equipamentos.models import Equipamento
from core.exceptions import EquipamentoUnavailable, DuplicateExecution
from core.services import executePedido, cancelPedido


class PedidoViewset(viewsets.ModelViewSet):
    """Viewset do model Pedido"""

    serializer_class = serializers.PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna os pedidos do usuário logado"""
        return Pedido.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Retorna o serializer class correto de acordo com a ação"""
        if self.action == 'create':
            return serializers.PedidoCreateSerializer
        if self.action == 'update':
            return serializers.PedidoUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Cria pedido definindo o user logado como dono"""
        return serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Checa se o pedido a ser cancelado aindo não foi executado"""
        instance = self.get_object()

        if instance.executed:
            return Response(
                'Não é possível deletar um pedido que está ou já foi ' +
                'executado! Cancele o pedido antes de deletá-lo.',
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_item(self, request, *args, **kwargs):
        """Adiciona um equipamento no pedido"""
        pedido = self.get_object()
        equipamento_id = request.data.get('equipamento')

        if equipamento_id is None:
            return Response(
                'O id do equipamento a ser adicionado deve ser passado com o' +
                'nome "equipamento"!',
                status=status.HTTP_400_BAD_REQUEST
            )

        equipamento = get_object_or_404(Equipamento, id=equipamento_id)
        pedido.equipamentos.add(equipamento)
        pedido.save()

        serializer = self.get_serializer_class()(pedido)
        return Response(data=serializer.data)

    @action(
        methods=['delete'],
        detail=True,
        url_path='equipamentos/(?P<equip_id>[^/.]+)',
        url_name='remove_item'
    )
    def remove_item(self, request, equip_id, *args, **kwargs):
        """Remove um equipamento do pedido"""
        pedido = self.get_object()

        try:
            equipamento = pedido.equipamentos.get(id=equip_id)
        except Equipamento.DoesNotExist:
            return Response(
                'O pedido já não continha esse equipamento',
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido.equipamentos.remove(equipamento)
        pedido.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def confirmation(self, request, *args, **kwargs):
        """Confirma o pedido e avança seu processamento no sistema"""
        pedido = self.get_object()

        try:
            executePedido(pedido)
        except (
            ValueError, EquipamentoUnavailable, DuplicateExecution
        ) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        pedido.save()
        return Response('Pedido confirmado!')

    @action(methods=['post'], detail=True)
    def cancelation(self, request, *args, **kwargs):
        """Cancela um pedido anteriormente confirmado"""
        pedido = self.get_object()

        try:
            cancelPedido(pedido)
        except DuplicateExecution as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        pedido.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

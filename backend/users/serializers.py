from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer do model User"""

    class Meta:
        model = User
        fields = ('id', 'name', 'email')

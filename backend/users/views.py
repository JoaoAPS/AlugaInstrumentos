from rest_framework import views, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.serializers import UserSerializer


class AuthTokenView(ObtainAuthToken):
    """Returna token de autenticação de um user com credenciais corretas"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'name': user.name,
        })


class UserRegisterView(views.APIView):
    """Registra um novo user"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        password1 = data.pop('password1')
        password2 = data.pop('password2')
        if type(password1) == list:
            password1 = password1[0]
        if type(password2) == list:
            password2 = password2[0]

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if not password1:
            return Response(
                {'password1': 'A senha deve ser definida.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if password2 != password1:
            return Response(
                {'password2': 'Os dois campos de senha devem ser iguais.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        user.set_password(password1)
        user.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'name': user.name,
        })

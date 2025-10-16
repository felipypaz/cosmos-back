# core/auth_email.py
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        User = get_user_model()
        email = attrs["email"].strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Usuário não encontrado."})
        except MultipleObjectsReturned:
            raise serializers.ValidationError({"email": "E-mail duplicado. Ajuste os cadastros."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Usuário inativo."})
        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Senha inválida."})

        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class EmailTokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        s = EmailTokenObtainPairSerializer(data=request.data, context={"request": request})
        s.is_valid(raise_exception=True)
        return Response(s.validated_data, status=status.HTTP_200_OK)

from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import CustomUser


class SignUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        ref_name = 'ReadOnlyUsers'

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" использовать нельзя.'
            )
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" использовать нельзя.'
            )
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'confirmation_code'
        )

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        confirmation_code = data.get('confirmation_code', None)

        if email is None:
            raise serializers.ValidationError(
                'Нужен email.'
            )

        if confirmation_code is None:
            raise serializers.ValidationError(
                'Нужен код подтверждения.'
            )

        user = authenticate(
            username=username,
            confirmation_code=confirmation_code
        )

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким email не найден.'
            )

        return {
            'username': user.username,
            'confirmation_code': user.confirmation_code
        }

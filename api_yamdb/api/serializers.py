from django.contrib.auth import authenticate
from pyexpat import model
from attr import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Genre, Category, Titles
from users.models import CustomUser
from reviews.models import Review


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
    token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'username', 'confirmation_code', 'token'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class CommentSerializer(serializers.ModelSerializer):

    pass

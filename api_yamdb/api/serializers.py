from django.db.models import Avg
from typing_extensions import Required
from django.contrib.auth import authenticate
from pyexpat import model
from attr import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Titles
from users.models import CustomUser
from reviews.models import Review, Comment


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


class GetPersonalAccountSerializers(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        if instance.role != CustomUser.ADMIN:
            attrs['role'] = instance.role
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    token = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = (
            'username', 'confirmation_code', 'token'
        )

    def validate(self, attrs):
        if not attrs.get('username'):
            raise ValueError('Введите имя пользователя.')
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        #fields = '__all__'
        fields = ('id', 'score', 'author', 'text', 'pub_date')
        model = Review


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitlesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', 'description')
        model = Titles

    def validate(self, data):
        name = data.get('name', None)

        if name is None:
            raise serializers.ValidationError(
                'Введите имя.'
            )
        return data

      
class TitleDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = GenreSerializer(
        many=True, read_only=True)

    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', 'description', 'rating')
        model = Titles

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        if rating['score__avg'] != None:
            return int(rating['score__avg'])
        return None

        
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        # fields = '__all__'
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment

from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from reviews.models import Comment, Genre, Category, Titles

from users.models import CustomUser
from .serializers import CustomUserSerializer, GenreSerializer
from .serializers import CategorySerializer, TitlesSerializer
from .serializers import ReviewSerializer, CommentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

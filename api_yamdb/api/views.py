from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from reviews.models import Comment

from users.models import CustomUser
from .serializers import CustomUserSerializer, ReviewSerializer, CommentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



from django.shortcuts import render
from rest_framework import viewsets, permissions, filters

from reviews.models import Comment, Genre, Category, Titles

from users.models import CustomUser
from .serializers import CustomUserSerializer, GenreSerializer
from .serializers import CategorySerializer, TitlesSerializer
from .serializers import ReviewSerializer, CommentSerializer

from reviews.models import Review
from reviews.models import Comment
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
=======

class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title)

    def destroy(self, request, title_id=None, pk=None):
        review = get_object_or_404(Review, id=pk)
        # self.check_object_permissions(self.request, comment)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


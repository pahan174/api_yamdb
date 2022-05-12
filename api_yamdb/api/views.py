
from multiprocessing import AuthenticationError
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Category, Comment, Genre, Review, Titles
from users.models import CustomUser
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerializer, GenreSerializer,
                          LoginSerializer, ReviewSerializer,
                          SignUserSerializer, TitlesSerializer)


from .permissions import OwnerOrReadOnly, AdminOrReadOnly


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    lookup_field = 'username'
    search_fields = ('username',)


@ action(detail=False, methods=['POST', 'PATCH'], name='me')
@ permission_classes([IsAuthenticated])
def get_personal_account(self, request):
    user = self.request.user
    if request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        serializer = CreateUserSerializer(user, data=request.data,
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
@ permission_classes([AllowAny])
def signup(request):
    serializer = SignUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user = get_object_or_404(CustomUser, username=username)
        confirmation_code = default_token_generator.make_token(user)
        serializer.save(email=email, confirmation_code=confirmation_code)

        send_mail(
            'Тема письма',
            f'Код подтверждения: {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
@ permission_classes([AllowAny])
def token_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = CustomUser.objects.get(username=username)
        token = RefreshToken.for_user(user)
        if user.confirmation_code == confirmation_code:
            return Response({'access': str(token.access_token)},
                            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    #pagination_classes = PageNumberPagination
    lookup_field = 'slug'
    search_fields = ('slug',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ('slug',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'category__slug', 'name', 'year')


class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadOnly, )
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
        self.check_object_permissions(self.request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadOnly, )
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review_id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Comment, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review)

    def destroy(self, request, title_id=None, pk=None):
        comment = get_object_or_404(Comment, id=pk)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

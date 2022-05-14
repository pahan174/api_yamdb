from django.urls import include, path
from rest_framework import routers

from . import views
from .views import (CategoryViewSet, CustomUserViewSet,
                    GenreViewSet, ReviewsViewSet,
                    TitlesViewSet, CommentViewSet)


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoryViewSet)

router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews_url')

router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments_url'
                )


urlpatterns = [
    path('users/me/', views.get_personal_account, name='me'),
    path('', include(router.urls)),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/token/', views.token_login, name='token')
]

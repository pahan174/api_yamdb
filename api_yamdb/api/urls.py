from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, GenreViewSet 
from .views import CategoryViewSet, TitlesViewSet


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('signup', views),
    # path('token/', views)
]

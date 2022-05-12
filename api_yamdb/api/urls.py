from django.urls import include, path
from rest_framework import routers

from . import views
from .views import CustomUserViewSet


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/token/', views.token_login, name='token')
]

from django.urls import include, path
from rest_framework import routers

from .views import GenreViewSet 
from .views import CategoryViewSet, TitlesViewSet

from .views import CustomUserViewSet, ReviewsViewSet



router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoryViewSet)
=======
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews_url')

urlpatterns = [
    path('', include(router.urls)),
    # path('signup', views),
    # path('token/', views)
]

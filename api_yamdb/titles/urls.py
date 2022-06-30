from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'titles', views.TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]

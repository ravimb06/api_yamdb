from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, signup_post, token_post,
                       ReviewViewSet, CommentViewSet)
from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet
app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/token/', token_post),
    path('v1/auth/signup/', signup_post),
    path('v1/', include(router.urls)),
]

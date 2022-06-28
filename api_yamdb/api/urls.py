from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet,
    signup_post,
    token_post,
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', token_post),
    path('v1/auth/signup/', signup_post),
    path('v1/', include(router.urls)),
]

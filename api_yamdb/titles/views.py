from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .mixins import CreateListDeleteViewSet
from .models import Category, Genre, Title
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleAdminSerializer, TitleReadOnlySerializer)


class CategoryViewSet(CreateListDeleteViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDeleteViewSet):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all()  # надо что-то с рейтингом придумать,ищу инфу
    pagination_class = PageNumberPagination
    ordering = ('name',)

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadOnlySerializer
        return TitleAdminSerializer

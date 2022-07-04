import uuid

from api.filters import TitleFilter
from api.permissions import (IsAdminModeratorAuthorOrReadOnly,
                             IsAdminOrReadOnly, OwnerOrAdmins)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MeSerializer, ReviewSerializer,
                             SignUpSerializer, TitleAdminSerializer,
                             TitleReadOnlySerializer, TokenSerializer,
                             UserSerializer)

from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from titles.mixins import CreateListDeleteViewSet
from titles.models import Category, Genre, Title

from users.models import User


@api_view(['POST'])
def signup_post(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, create = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response(
            'Такой логин или email уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подверждения', confirmation_code,
        None, (user.email, )
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_post(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user_base = get_object_or_404(User, username=username)
    if confirmation_code == user_base.confirmation_code:
        token = str(AccessToken.for_user(user_base))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins, )
    filter_backends = (SearchFilter,)
    filterset_fields = ('username')
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDeleteViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDeleteViewSet):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadOnlySerializer
        return TitleAdminSerializer

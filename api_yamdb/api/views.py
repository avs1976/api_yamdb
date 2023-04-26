from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User

from .permissions import (IsAdmin, IsAdminModeratorAuthorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleGenreReadSerializer,
                          TitleReadSerializer, TitleSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)


@api_view(['POST'])
def register_user(request, id='id'):
    """Функция регистрации user, генерации и отправки кода на почту"""

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError(
            'username или email заняты!', status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """Функция выдачи токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def get_edit_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(review=review, title=title)


class NoPatchMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод PATCH запрещен для данного ресурса.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CategoryViewSet(NoPatchMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        queryset = self.queryset
        genre_slug = self.request.query_params.get('genre', None)
        if genre_slug is not None:
            genre = get_object_or_404(Genre, slug=genre_slug)
            queryset = queryset.filter(genre=genre)

        category_slug = self.request.query_params.get('category', None)
        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
        if getattr(serializer.instance, '_prefetched_objects_cache', None):
            serializer.instance._prefetched_objects_cache = {}
            
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def handle_exception(self, exc):
        if isinstance(exc, MethodNotAllowed) and self.request.method == 'PATCH':
            return Response({'detail': 'PATCH метод не разрешен.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif isinstance(exc, MethodNotAllowed) and self.request.method == 'GET':
            return Response({'detail': 'GET метод не разрешен.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)


class TitleGenreViewSet(viewsets.ModelViewSet):
    queryset = TitleGenre.objects.prefetch_related('genre', 'title').all()
    serializer_class = TitleGenreReadSerializer
    permission_classes = [IsAdminOrReadOnly]


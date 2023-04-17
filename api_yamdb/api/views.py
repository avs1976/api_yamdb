from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from reviews.models import Category, Genre, Title, TitleGenre

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGenreReadSerializer,
                          TitleGenreWriteSerializer, TitleReadSerializer,
                          TitleWriteSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)


class TitleGenreViewSet(viewsets.ModelViewSet):
    queryset = TitleGenre.objects.prefetch_related('genre', 'title').all()
    serializer_class = TitleGenreReadSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

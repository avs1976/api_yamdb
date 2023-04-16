from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from reviews.models import Category, Genre, Review, Title, TitleGenre

from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, TitleGenreReadSerializer,
                          TitleGenreWriteSerializer, TitleReadSerializer,
                          TitleWriteSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Review.objects.select_related('title').all()
        title_id = self.request.query_params.get('title_id', None)
        if title_id is not None:
            queryset = queryset.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)


class TitleGenreViewSet(viewsets.ModelViewSet):
    queryset = TitleGenre.objects.prefetch_related('genre', 'title').all()
    serializer_class = TitleGenreReadSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

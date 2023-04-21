from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

routerv1 = DefaultRouter()

routerv1.register('genres', GenreViewSet, basename='genres')
routerv1.register('categories', CategoryViewSet, basename='categories')
routerv1.register('titles', TitleViewSet, basename='titles')
routerv1.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
routerv1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                  CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(routerv1.urls)),
]

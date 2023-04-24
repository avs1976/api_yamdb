from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,  get_token,
                    register_user)

app_name = 'api'

routerv1 = DefaultRouter()

routerv1.register(r'users', UserViewSet, basename='users')
routerv1.register('genres', GenreViewSet, basename='genres')
routerv1.register('categories', CategoryViewSet, basename='categories')
routerv1.register('titles', TitleViewSet, basename='titles')
routerv1.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
routerv1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns_auth = [
    path('signup/', register_user, name='register_user'),
    path('token/', get_token, name='token'),
]
urlpatterns = [
    path('v1/', include(routerv1.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

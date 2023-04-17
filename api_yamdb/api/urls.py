from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet


routerv1 = DefaultRouter()
routerv1.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
routerv1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                  CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(routerv1.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategorieViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserCreateViewSet,
                       UserTokenViewSet, UserViewSet)

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategorieViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title>[0-9]+)/reviews',
                   ReviewViewSet, basename='review_v1')
v1_router.register(
    r'titles/(?P<title>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment_v1'
)

v1_urlpatterns = [
    path(
        'auth/signup/',
        UserCreateViewSet.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        UserTokenViewSet.as_view(),
        name='token'
    ),
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserCreateViewSet, UserTokenViewSet, UserViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')

v1_urlpatterns = [
    path(
        'auth/signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'auth/token/',
        UserTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]

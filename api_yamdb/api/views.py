from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError


from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAdmin, IsAuthenticatedForPut
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleGetSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)

from reviews.models import Category, Genre, Title, Review, Comment
from api.serializers import (UserCreateSerializer, UserSerializer,
                             UserTokenSerializer)
from api.utils import send_confirmation_code

User = get_user_model()


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTokenViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Неверный код подтверждения.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


ALLOWED_METHODS = ['get', 'post', 'patch', 'delete']


class CategorieViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """Получаем/создаем/удаляем категорию."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewset(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Получаем/создаем/удаляем жанр."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем произведение."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ALLOWED_METHODS

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedForPut, )

    def get_queryset(self):
        return self.get_title(self.kwargs['title_id']).reviews.all()

    def get_title(self, title_id):
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        title_id = self.get_title(self.kwargs['title_id'])
        user = self.request.user
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise ValidationError({'detail': 'Отзыв уже существует.'})
        serializer.save(author=self.request.user, title_id=title_id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.author != self.request.user
                and not self.request.user.is_moderator
                and not self.request.user.is_admin):
            return Response({'detail': 'Нет прав на редактирование.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance,
                                         data=self.request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        super().perform_update(serializer)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Метод PUT не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_destroy(self, instance):
        if (instance.author != self.request.user
                and not self.request.user.is_moderator
                and not self.request.user.is_admin):
            raise PermissionDenied('У Вас нет прав, на удаление.')
        super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedForPut, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self, review_id):
        return get_object_or_404(Review, pk=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review(self.kwargs['review_id']))

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.author == self.request.user
                or self.request.user.is_moderator
                or self.request.user.is_admin):
            serializer = self.get_serializer(instance,
                                             data=self.request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            super().perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Нет прав на редактирование.'},
                        status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Метод PUT не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_destroy(self, instance):
        if (instance.author != self.request.user
                and not self.request.user.is_moderator
                and not self.request.user.is_admin):
            raise PermissionDenied('У Вас нет прав, на удаление.')
        super().perform_destroy(instance)

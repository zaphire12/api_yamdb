from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class ReviewCommentUpdateMixin(viewsets.ModelViewSet):

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

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class IsAdvertisementOwner(BasePermission):
    """Разрешает изменение объекта только его автору."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = (
        DjangoFilterBackend,
    )

    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            return [
                IsAuthenticated(),
            ]

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsAdvertisementOwner(),
            ]

        return []

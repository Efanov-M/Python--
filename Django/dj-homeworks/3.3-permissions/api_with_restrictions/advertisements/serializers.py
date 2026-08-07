from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import (
    Advertisement,
    AdvertisementStatusChoices,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Создание объявления."""

        validated_data["creator"] = self.context["request"].user

        return super().create(validated_data)

    def validate(self, data):
        """Проверка количества открытых объявлений пользователя."""

        request = self.context["request"]
        user = request.user

        if self.instance:
            new_status = data.get(
                "status",
                self.instance.status,
            )
        else:
            new_status = data.get(
                "status",
                AdvertisementStatusChoices.OPEN,
            )

        if new_status == AdvertisementStatusChoices.OPEN:
            opened_ads = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN,
            )

            if self.instance:
                opened_ads = opened_ads.exclude(
                    pk=self.instance.pk
                )

            if opened_ads.count() >= 10:
                raise serializers.ValidationError(
                    "У пользователя не может быть больше "
                    "10 открытых объявлений."
                )

        return data

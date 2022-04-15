from rest_framework import serializers

from mailing.models import Mailings, Users, Messages


class MailingsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылкок
    """

    class Meta:
        model = Mailings
        fields = ("id", "text", "date_time_start")


class MailingDetailSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылки детально
    """

    class Meta:
        model = Mailings
        fields = "__all__"


class MailingsCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылки детально
    """

    class Meta:
        model = Mailings
        fields = "__all__"

    def create(self, validated_data):
        return Mailings.objects.create(**validated_data)


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериалайзер пользователей
    """

    class Meta:
        model = Users
        exclude = ("last_update",)


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер создания пользователя
    """

    class Meta:
        model = Users
        exclude = ("last_update",)

    def create(self, validated_data):
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class MessagesSerializer(serializers.ModelSerializer):
    """
    Сериалайзер сообщений
    """
    mailing = serializers.SlugRelatedField(slug_field="text", read_only=True)
    user = serializers.SlugRelatedField(slug_field="number", read_only=True)

    class Meta:
        model = Messages
        exclude = ("last_update",)

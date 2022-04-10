from rest_framework import serializers

from mailing.models import Mailings, Users, Messages


class MailingsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылкок
    """

    class Meta:
        model = Mailings
        fields = ("text", "date_time_start")


class MailingsDetailSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылки детально
    """

    class Meta:
        model = Mailings
        exclude = ()


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериалайзер пользователей
    """

    class Meta:
        model = Users
        exclude = ("last_update",)


class MessagesSerializer(serializers.ModelSerializer):
    """
    Сериалайзер сообщений
    """
    mailing = serializers.SlugRelatedField(slug_field="text", read_only=True)
    user = serializers.SlugRelatedField(slug_field="number", read_only=True)

    class Meta:
        model = Messages
        exclude = ("last_update",)

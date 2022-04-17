from datetime import datetime

from rest_framework import serializers

from mailing.models import Mailings, Users, Messages


class MailingsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер рассылкок
    """

    class Meta:
        model = Mailings
        fields = ("id", "text", "date_time_start", "done")


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

    def validate(self, data):
        if data["date_time_start"] > data["date_time_finish"]:
            raise serializers.ValidationError("Date start is more date finish wrong")
        return data


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

    def validate(self, data):
        if data['number'] > 79999999999 or data['number'] < 70000000000:
            raise serializers.ValidationError("Number is wrong")
        return data


class MessagesSerializer(serializers.ModelSerializer):
    """
    Сериалайзер сообщений
    """
    mailing_text = serializers.SlugRelatedField(slug_field="text", read_only=True)
    user = serializers.SlugRelatedField(slug_field="number", read_only=True)

    class Meta:
        model = Messages
        exclude = ("last_update",)

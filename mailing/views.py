from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mailings, Users, Messages
from .serializers import MailingsSerializer, UsersSerializer, MailingsDetailSerializer, MessagesSerializer


class MailingsListView(APIView):
    """
    Вывод всех рассылок из БД.
    """

    def get(self, request):
        mailings = Mailings.objects.all()
        seriolazer = MailingsSerializer(mailings, many=True)
        return Response(seriolazer.data)


class MailingDetailListView(APIView):
    """
    Вывод деталей рассылки из БД.
    """

    def get(self, request, pk):
        mailings = Mailings.objects.get(id=pk)
        seriolazer = MailingsDetailSerializer(mailings)
        return Response(seriolazer.data)


class UsersListView(APIView):
    """
    Вывод всех пользователей из БД.
    """

    def get(self, request):
        users = Users.objects.filter(active=True)
        seriolazer = UsersSerializer(users, many=True)
        return Response(seriolazer.data)


class MessageListView(APIView):
    """
    Вывод всех Сообщений из БД.
    """

    def get(self, request):
        messages = Messages.objects.all()
        seriolazer = MessagesSerializer(messages, many=True)
        return Response(seriolazer.data)

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mailings, Users, Messages
from .serializers import MailingsSerializer, UsersSerializer, MailingDetailSerializer, MessagesSerializer, \
    UserCreateUpdateSerializer, MailingsCreateSerializer
from .tasks_mailing import send_mailing


class MailingsListView(APIView):
    """
    Вывод всех рассылок из БД.
    """

    def get(self, request):
        mailings = Mailings.objects.all()
        seriolazer = MailingsSerializer(mailings, many=True)
        return Response(seriolazer.data, status=200)


class MailingDetailView(APIView):
    """
    Вывод деталей рассылки из БД.
    """

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method GET is not allowed"}, status=400)
        try:
            mailings = Mailings.objects.get(id=pk)
        except:
            return Response({"error": "Object does not exists"}, status=400)
        seriolazer = MailingDetailSerializer(mailings)
        return Response(seriolazer.data, status=200)


class MailingCreateView(APIView):
    """
    Создание записи в таблице рассылок в БД.
    """

    def post(self, request):
        mailing = MailingsCreateSerializer(data=request.data)
        if mailing.is_valid(raise_exception=True):
            mailing.save()
            # print(mailing.data["id"])
            # print("---------")
            # print(mailing.data["date_time_start"])
            # print("---------")
            # print(mailing.data["date_time_finish"])
            # print("---------")
            # print(mailing.data)
            send_mailing.apply_async(args=[mailing.data["id"], ], eta=mailing.data["date_time_start"])
            return Response(mailing.data, status=200)

        return Response({"error": "Bad request"}, status=400)


class UsersListView(APIView):
    """
    Вывод всех пользователей из БД.
    """

    def get(self, request):
        users = Users.objects.filter(active=True)
        seriolazer = UsersSerializer(users, many=True)
        return Response(seriolazer.data, status=200)


class UserCreateUpdateView(APIView):
    """
    Вывод всех пользователей из БД.
    """

    def post(self, request):

        new_user = UserCreateUpdateSerializer(data=request.data)
        if new_user.is_valid(raise_exception=True):
            new_user.save()
            return Response({"post": new_user.data}, status=201)
        return Response({"error": "Bad request"}, status=400)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"}, status=400)

        try:
            instance = Users.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"}, status=400)
        update_user = UserCreateUpdateSerializer(instance=instance, data=request.data)
        update_user.is_valid(raise_exception=True)
        update_user.save()

        return Response({"put": update_user.data}, status=202)


class MessageListView(APIView):
    """
    Вывод всех Сообщений из БД.
    """

    def get(self, request):
        messages = Messages.objects.all()
        seriolazer = MessagesSerializer(messages, many=True)
        return Response(seriolazer.data, status=200)

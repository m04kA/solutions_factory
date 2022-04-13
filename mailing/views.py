from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mailings, Users, Messages
from .serializers import MailingsSerializer, UsersSerializer, MailingsDetailSerializer, MessagesSerializer, \
    UserCreateUpdateSerializer


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


class UserCreateUpdateView(APIView):
    """
    Вывод всех пользователей из БД.
    """

    def post(self, request):

        new_user = UserCreateUpdateSerializer(data=request.data)
        if new_user.is_valid():
            new_user.save()
            return Response({"post": new_user.data}, status=201)
        return Response({"error": "Bad request"}, status=400)

    def put(self, request, *args, **kwargs):
        # print(args)
        # print('---------')
        # print(kwargs)
        # print('---------')
        pk = kwargs.get('pk', None)
        # print(pk)
        if not pk:
            return Response({"error": "Method PUT is not allowed"}, status=400)

        try:
            instance = Users.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"}, status=400)
        # gg = UsersSerializer(instance)
        # print(instance.number)
        update_user = UserCreateUpdateSerializer(instance=instance, data=request.data)
        update_user.is_valid(raise_exception=True)
        update_user.save()
        # print(update_user.data)
        # gg = UsersSerializer(update_user)
        # print(gg.data)
        # if update_user.is_valid():
        #     update_user.save()

        return Response({"put": update_user.data}, status=202)


class MessageListView(APIView):
    """
    Вывод всех Сообщений из БД.
    """

    def get(self, request):
        messages = Messages.objects.all()
        seriolazer = MessagesSerializer(messages, many=True)
        return Response(seriolazer.data)

from datetime import datetime, timedelta

from django.db.models import Q
from psycopg2 import tz
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mailings, Users, Messages
from .serializers import MailingsSerializer, UsersSerializer, MailingDetailSerializer, MessagesSerializer, \
    UserCreateUpdateSerializer, MailingsCreateSerializer
from .tasks import send_mailing

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger("mailing")


class MailingsListView(APIView):
    """
    Вывод всех рассылок из БД.
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                        "date_time_start": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                        "done": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "success_message": openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        logger.info("Get info about all mailings")
        mailings = Mailings.objects.all()
        seriolazer = MailingsSerializer(mailings, many=True).data
        count = 0
        for mailing in mailings:
            if mailing.done:
                messages_all = len(Messages.objects.filter(mailing_text=mailing))
                messages_done = len(Messages.objects.filter(Q(mailing_text=mailing) & Q(success=True)))
                seriolazer[count]["success_message"] = f"{messages_done} / {messages_all}"
            count += 1
        return Response(seriolazer, status=200)


class MailingDetailView(APIView):
    """
    Вывод деталей рассылки из БД.
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "date_time_start": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "date_time_finish": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                    "filter_info": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                    "done": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "last_update": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "messages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "date_time": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "mailing_text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                                "user": openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            logger.error(f"Bad request for detail info about mailing.")
            return Response({"error": "Method GET is not allowed"}, status=400)
        try:
            logger.info(f"Get detail info about mailing (id - {pk})")
            mailing = Mailings.objects.get(id=pk)
        except Mailings.DoesNotExist:
            logger.error(f"Mailing (id - {pk}) does not exists")
            return Response({"error": "Object does not exists"}, status=400)
        seriolazer = MailingDetailSerializer(mailing).data
        messages_all = Messages.objects.filter(mailing_text=mailing)
        messages_all = MessagesSerializer(messages_all, many=True).data
        seriolazer["messages"] = messages_all
        return Response(seriolazer, status=200)


class MailingDeleteView(APIView):
    """
    Удаление рассылки из БД.
    """

    @swagger_auto_schema(
        responses={
            204: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "date_time_start": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "date_time_finish": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                    "filter_info": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                    "done": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "last_update": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "messages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "date_time": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "mailing_text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                                "user": openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            logger.error(f"Bad request for DELETE mailing.")
            return Response({"error": "Method DELETE is not allowed"}, status=400)
        try:
            logger.info(f"Get detail info about mailing (id - {pk})")
            mailing = Mailings.objects.get(id=pk)
        except Mailings.DoesNotExist:
            logger.error(f"Mailing (id - {pk}) does not exists")
            return Response({"error": "Object does not exists"}, status=400)
        seriolazer = MailingDetailSerializer(mailing).data
        logger.info(f"Get info about MESSAGES (mailing id - {mailing.id})")
        messages_all = Messages.objects.filter(mailing_text=mailing)
        messages_all = MessagesSerializer(messages_all, many=True).data
        seriolazer["messages"] = messages_all
        mailing.delete()
        logger.info(f"Delete mailing (id - {pk}) and messages")
        return Response(seriolazer, status=204)


class MailingCreateView(APIView):
    """
    Создание записи в таблице рассылок в БД.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "date_time_start": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                "date_time_finish": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                "text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                "filter_info": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
            }
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "date_time_start": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "date_time_finish": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    "text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                    "filter_info": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                    "done": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "last_update": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        try:
            mailing = MailingsCreateSerializer(data=request.data)
            if mailing.is_valid(raise_exception=True):
                mailing.save()
                logger.info(f"Create mailing (id - {mailing.data['id']})")
                date_start = mailing.data["date_time_start"]
                date_start = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=3)
                send_mailing.apply_async(args=(mailing.data["id"],), eta=date_start)
                logger.info(f"Create task for celery. It will start {date_start + timedelta(hours=3)}")
                return Response(mailing.data, status=201)
            logger.error(f"Bad request for create mailing data: {request.data}")
            return Response({"error": "Bad request"}, status=400)
        except:
            logger.error(f"Bad request for create mailing data: {request.data}")
            return Response({"error": "Bad request"}, status=400)


class UsersListView(APIView):
    """
    Вывод всех пользователей из БД.
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                        "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                        "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
                        "active": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            )
        }
    )
    def get(self, request):
        logger.info("Get info about all users")
        users = Users.objects.filter(active=True)
        seriolazer = UsersSerializer(users, many=True)
        return Response(seriolazer.data, status=200)


class UserCreateView(APIView):
    """
    Создание пользователя.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
            }
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "post": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
                            "active": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                        }
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        try:
            new_user = UserCreateUpdateSerializer(data=request.data)
            if new_user.is_valid(raise_exception=True):
                new_user.save()
                logger.info(f"Create user (id - {new_user.data['id']})")
                return Response({"post": new_user.data}, status=201)
            logger.error(f"Bad request for create mailing data: {request.data}")
            return Response({"error": "Bad request"}, status=400)
        except:
            logger.error(f"Bad request for create mailing data: {request.data}")
            return Response({"error": "Bad request"}, status=400)


class UserUpdateView(APIView):
    """
    Обновление данных пользователя.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
            }
        ),
        responses={
            202: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "put": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
                            "active": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                        }
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            logger.error(f"Bad request for update user. data: {request.data}")
            return Response({"error": "Method PUT is not allowed"}, status=400)
        try:
            logger.info(f"Get detail info about user (id - {pk})")
            instance = Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            logger.error(f"User (id - {pk}) does not exists")
            return Response({"error": "Object does not exists"}, status=400)
        update_user = UserCreateUpdateSerializer(instance=instance, data=request.data)
        update_user.is_valid(raise_exception=True)
        update_user.save()
        logger.info(f"Successful update user (id - {pk})")
        return Response({"put": update_user.data}, status=202)


class UserDeleteView(APIView):
    """
    Удаление пользователя.
    """

    @swagger_auto_schema(
        responses={
            202: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "delete": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "code_mob_opr": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "teg": openapi.Schema(type=openapi.TYPE_STRING, max_length=25),
                            "time_zone": openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
                            "active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "messages": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "date_time": openapi.Schema(type=openapi.TYPE_STRING,
                                                                    format=openapi.FORMAT_DATE),
                                        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                        "mailing_text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                                        "user": openapi.Schema(type=openapi.TYPE_INTEGER)
                                    }
                                )
                            )
                        }
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            logger.error(f"Bad request for update user. data: {request.data}")
            return Response({"error": "Method DELETE is not allowed"}, status=400)

        try:
            logger.info(f"Get detail info about user (id - {pk})")
            instance = Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            logger.error(f"User (id - {pk}) does not exists")
            return Response({"error": "Object does not exists"}, status=400)
        update_user = UsersSerializer(instance).data
        messages = Messages.objects.filter(user=instance)
        seriolazer = MessagesSerializer(messages, many=True).data
        update_user["messages"] = seriolazer
        instance.delete()
        logger.info(f"Successful delete user (id - {pk})")
        return Response({"delete": update_user}, status=202)


class MessageListView(APIView):
    """
    Вывод всех Сообщений из БД.
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "date_time": openapi.Schema(type=openapi.TYPE_STRING,
                                                    format=openapi.FORMAT_DATE),
                        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "mailing_text": openapi.Schema(type=openapi.TYPE_STRING, max_length=300),
                        "user": openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            )
        }
    )
    def get(self, request):
        logger.info("Get info about all messages.")
        messages = Messages.objects.all()
        seriolazer = MessagesSerializer(messages, many=True)
        return Response(seriolazer.data, status=200)

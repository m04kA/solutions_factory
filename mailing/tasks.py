from django.db.models import Q
import json as JSON
from solutions_factory.celery import app
from .serializers import MailingDetailSerializer, UsersSerializer
from .models import Mailings, Users, Messages
from requests import Session
import datetime
import logging

logger = logging.getLogger("mailing")


@app.task
def send_mailing(mailing_id: int):
    logger.info(f"Start mailing (id - {mailing_id})")
    try:
        logger.info(f"Get detail info about mailing (id - {mailing_id})")
        mailing = Mailings.objects.get(id=mailing_id)
        mailing_data = MailingDetailSerializer(mailing).data
        logger.info(f"Get info about users (code_mob_opr={mailing_data['filter_info']} or teg={mailing_data['filter_info']})")
        users = Users.objects.filter(Q(code_mob_opr=mailing_data["filter_info"]) | Q(teg=mailing_data["filter_info"]))
        users = UsersSerializer(users, many=True).data
        session = Session()
        headers = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODA2MTAxNDUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Illhcm9zbGF2UGFuYXJpbiJ9.ASun1vCxgdLxTphbaON_K2OoiZIrAw1fFDcQbu3WZRw",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        session.headers.update(headers)
        date_finish = mailing_data["date_time_finish"]
        date_finish = datetime.datetime.strptime(date_finish, '%Y-%m-%dT%H:%M:%SZ')
        for user in users:
            if datetime.datetime.now() < date_finish:
                url = f"https://probe.fbrq.cloud/v1/send/{user['id']}"
                data = {
                    "id": user['id'],
                    "phone": user['number'],
                    "text": mailing_data['text']
                }
                logger.info(f"Request to other API (user_id - {data['id']}, text - {data['text']})")
                response = session.request(
                    method="POST",
                    url=url,
                    json=data,
                    timeout=5
                )
                user = Users.objects.get(id=user["id"])
                if response.status_code == 200:
                    logger.info(f"Create message (mailing_id - {mailing_data['id']}, user_id - {data['id']})")
                    message = Messages(success=True, mailing_text=mailing, user=user)
                    message.save()
                    continue
                logger.error(f"Error create message (mailing_id - {mailing_data['id']}, user_id - {data['id']})")
                message = Messages(success=False, mailing_text=mailing, user=user)
                message.save()
            else:
                logger.info(f"Time`s up message (mailing_id - {mailing_data['id']}, user_id - {user['id']})")
                message = Messages(success=False, mailing_text=mailing, user=user)
                message.save()
        mailing.done = True
        mailing.save()
    except Mailings.DoesNotExist:
        logger.error(f"Mailing (id - {mailing_id}) does not exists")

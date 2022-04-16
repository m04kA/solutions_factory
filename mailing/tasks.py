from django.db.models import Q
import json as JSON
from solutions_factory.celery import app
from .serializers import MailingDetailSerializer, UsersSerializer
from .models import Mailings, Users, Messages
from requests import Session
import datetime


@app.task
def send_mailing(mailing_id: int):
    try:
        mailing = Mailings.objects.get(id=mailing_id)
        mailing_data = MailingDetailSerializer(mailing).data
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
                response = session.request(
                    method="POST",
                    url=url,
                    json=data,
                    timeout=5
                )
                user = Users.objects.get(id=user["id"])
                if response.status_code == 200:
                    message = Messages(success=True, mailing=mailing, user=user)
                    message.save()
                    continue

                message = Messages(success=False, mailing=mailing, user=user)
                message.save()
            else:
                message = Messages(success=False, mailing=mailing, user=user)
                message.save()
        mailing.done = True
        mailing.save()
    except Mailings.DoesNotExist:
        print(f"Mailing does not exists id - {mailing_id}")

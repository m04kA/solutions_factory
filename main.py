import os

import django.conf
from django.core.wsgi import get_wsgi_application

django.conf.ENVIRONMENT_VARIABLE = 'solutions_factory'
os.environ.setdefault('solutions_factory', "solutions_factory.settings")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

application = get_wsgi_application()

from mailing.models import Mailings, Users, Messages
import datetime

date = datetime.datetime.now() + datetime.timedelta(days=10)

print(date)
#
# data = Mailings(date_time_start=datetime.datetime.now(), date_time_finish=date, text="hi", filter_info="915", )
# data.save()
# data = Users(number=79998886655, code_mob_opr='999', teg='cat', time_zone='UTC')
# data.save()
# data = Users(number=75553336655, code_mob_opr='555', teg='cat', time_zone='UTC')
# data.save()
# data = Users(number=74442226655, code_mob_opr='444', teg='dog', time_zone='UTC')
# data.save()
# data = Users(number=76783336655, code_mob_opr='678', teg='car', time_zone='UTC', active=False)
# data.save()

data = Messages(success=True, mailing=Mailings.objects.get(text="hi"), user=Users.objects.get(number=79998886655))
data.save()

data = Messages(success=True, mailing=Mailings.objects.get(text="hi"), user=Users.objects.get(number=75553336655))
data.save()

data = Messages(success=False, mailing=Mailings.objects.get(text="hi"),
                user=Users.objects.get(number=74442226655))
data.save()

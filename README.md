Comands for starting:
1) pip install -r requirements.txt
2) Connecting DB (PostgreSQL) to Django in settings
3) python manage.py makemigrations
4) python manage.py migrate
5) python manage.py createsuperuser
6) Install docker for next step
7) docker run -d --name clever_hopper -p 6379:6379 redis / docker start clever_hopper
8) celery --app solutions_factory worker --pool=solo --loglevel=INFO
9) python manage.py runserver

celery -A solutions_factory flower - не работает

You can use super User:
    login: admin
    password: admin

My project working according to Moscow time.

http://127.0.0.1:8000/swagger/ - openApi
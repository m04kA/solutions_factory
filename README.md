Comands for starting:
1) pip install -r requirements.txt
2) create dir "logs" in ROOT_DIR
3) Connecting DB (PostgreSQL) to Django in settings
4) python manage.py makemigrations
5) python manage.py migrate
6) python manage.py createsuperuser
7) Install docker for next step
8) docker run -d --name clever_hopper -p 6379:6379 redis / docker start clever_hopper
9) celery --app solutions_factory worker --pool=solo --loglevel=INFO
10) python manage.py runserver

celery -A solutions_factory flower - не работает

You can use super User:
    login: admin
    password: admin

My project working according to Moscow time.

http://127.0.0.1:8000/swagger/ - openApi

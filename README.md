Comands:
celery --app solutions_factory worker --pool=solo --loglevel=INFO
docker run -d --name clever_hopper -p 6379:6379 redis / docker start clever_hopper
celery -A solutions_factory flower
python manage.py runserver
pip install -r requirements.txt
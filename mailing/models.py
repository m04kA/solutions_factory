from django.db import models
from datetime import datetime

from django.db.models import Q


class Mailings(models.Model):
    """
    Сущность рассылка.
    """
    date_time_start = models.DateTimeField("Время и дата старта")
    date_time_finish = models.DateTimeField("Время и дата конца")
    text = models.TextField("Текст", max_length=300)
    filter_info = models.CharField("Фильтр", max_length=25)
    done = models.BooleanField("Выполнено", default=False)
    last_update = models.DateTimeField("Дата последнего обновления", auto_now=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Users(models.Model):
    """
    Сущность пользователь.
    """
    number = models.PositiveBigIntegerField("Телефон", unique=True)
    code_mob_opr = models.CharField("Код оператора", max_length=25)
    teg = models.CharField("Тег", max_length=25)
    time_zone = models.CharField("Часовой пояс", max_length=10)
    last_update = models.DateTimeField("Дата последнего обновления", auto_now=True)
    active = models.BooleanField("Активность", default=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Messages(models.Model):
    """
    Сущность сообщение.
    """
    date_time = models.DateTimeField("Дата создания/отправки", default=datetime.now())
    success = models.BooleanField("Статус отправки", default=False)
    mailing_text = models.ForeignKey(Mailings, verbose_name="Связанная рассылка", on_delete=models.CASCADE, related_name="mailing_msg")
    user = models.ForeignKey(Users, verbose_name="Связанный пользователь", on_delete=models.CASCADE, related_name="user_msg")
    last_update = models.DateTimeField("Дата последнего обновления", auto_now=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

# Generated by Django 4.0.3 on 2022-04-15 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_alter_messages_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailings',
            name='done',
            field=models.BooleanField(default=False, verbose_name='Выполнено'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 15, 16, 53, 38, 389786), verbose_name='Дата создания/отправки'),
        ),
    ]
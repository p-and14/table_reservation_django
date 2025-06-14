# Generated by Django 5.2 on 2025-04-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['id'], 'verbose_name': 'Бронь', 'verbose_name_plural': 'Брони'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ['id'], 'verbose_name': 'Стол', 'verbose_name_plural': 'Столы'},
        ),
        migrations.AlterField(
            model_name='table',
            name='seats',
            field=models.PositiveSmallIntegerField(db_index=True, verbose_name='Количество мест'),
        ),
    ]

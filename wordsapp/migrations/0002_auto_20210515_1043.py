# Generated by Django 3.1.7 on 2021-05-15 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Описание'),
        ),
    ]

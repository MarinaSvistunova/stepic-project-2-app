# Generated by Django 3.0.5 on 2020-04-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0010_auto_20200418_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='salary',
            field=models.IntegerField(max_length=10),
        ),
    ]

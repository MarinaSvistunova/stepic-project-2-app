# Generated by Django 3.0.5 on 2020-04-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0011_auto_20200418_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='salary',
            field=models.IntegerField(),
        ),
    ]

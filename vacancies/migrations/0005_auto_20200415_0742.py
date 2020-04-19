# Generated by Django 3.0.5 on 2020-04-15 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0004_auto_20200415_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='60x60.png', upload_to='MEDIA_COMPANY_IMAGE_DIR'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(default='60x60.png', upload_to='MEDIA_SPECIALITY_IMAGE_DIR'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(default=1581491264, on_delete=django.db.models.deletion.CASCADE, related_name='company_vacancies', to='vacancies.Company'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='specialty',
            field=models.ForeignKey(default=1581491264, on_delete=django.db.models.deletion.CASCADE, related_name='speciality_vacancies', to='vacancies.Specialty'),
        ),
    ]

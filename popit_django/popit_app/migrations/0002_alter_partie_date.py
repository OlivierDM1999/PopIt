# Generated by Django 3.2.12 on 2022-05-05 12:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('popit_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partie',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

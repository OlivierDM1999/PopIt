# Generated by Django 3.2.12 on 2022-05-20 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit_app', '0004_joueur_pseudo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modele',
            name='lien',
        ),
        migrations.AddField(
            model_name='modele',
            name='lien_pb',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='modele',
            name='lien_pkl',
            field=models.CharField(default='', max_length=255),
        ),
    ]
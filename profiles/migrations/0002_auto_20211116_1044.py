# Generated by Django 3.2.7 on 2021-11-16 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimages',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='UserCredits',
        ),
    ]

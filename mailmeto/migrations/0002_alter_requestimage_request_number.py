# Generated by Django 3.2.7 on 2021-11-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailmeto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestimage',
            name='request_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-15 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0004_remove_client_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carte',
            name='date_exp',
            field=models.IntegerField(),
        ),
    ]

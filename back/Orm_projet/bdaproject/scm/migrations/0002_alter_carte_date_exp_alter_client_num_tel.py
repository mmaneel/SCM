# Generated by Django 5.0.6 on 2024-05-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carte',
            name='date_exp',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='client',
            name='num_tel',
            field=models.CharField(max_length=255),
        ),
    ]

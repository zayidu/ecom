# Generated by Django 3.0.9 on 2020-08-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

# Generated by Django 4.2.4 on 2023-10-23 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='kind',
            field=models.CharField(max_length=8),
        ),
    ]
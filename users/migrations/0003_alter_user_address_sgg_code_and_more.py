# Generated by Django 4.2.4 on 2023-09-12 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_address_sido_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address_sgg_code',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address_sido_code',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
# Generated by Django 4.2.4 on 2023-11-06 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0006_remove_resume_address2_sgg_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
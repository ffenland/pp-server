# Generated by Django 4.2.4 on 2023-09-19 05:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_resume_address2_sgg_code_resume_address2_sido_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='만든날짜'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='변경날짜'),
        ),
    ]
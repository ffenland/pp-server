# Generated by Django 4.2.4 on 2023-11-08 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_user_college_remove_user_year_of_admission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='ds', max_length=8),
            preserve_default=False,
        ),
    ]

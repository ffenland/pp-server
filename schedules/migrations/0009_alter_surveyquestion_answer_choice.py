# Generated by Django 4.2.4 on 2023-11-07 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0008_surveyanswer_surveyquestion_surveyresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='answer_choice',
            field=models.ManyToManyField(to='schedules.surveyanswer'),
        ),
    ]

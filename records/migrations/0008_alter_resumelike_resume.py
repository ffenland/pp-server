# Generated by Django 4.2.4 on 2023-11-06 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_resume_is_active'),
        ('records', '0007_resumelike_delete_resumerecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumelike',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedules.resume'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-04 05:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=9)),
                ('am', models.BooleanField(default=True)),
                ('pm', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('days', models.ManyToManyField(to='schedules.day')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('schedule', models.ManyToManyField(to='schedules.schedule')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

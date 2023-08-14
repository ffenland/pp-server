# Generated by Django 4.2.4 on 2023-08-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='title',
            new_name='article',
        ),
        migrations.AddField(
            model_name='post',
            name='kind',
            field=models.CharField(choices=[('question', '질문'), ('life', '일상'), ('info', '정보')], default='title', max_length=8),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-17 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('title', models.CharField(max_length=30)),
                ('kind', models.CharField(choices=[('question', '질문'), ('life', '일상'), ('info', '정보')], max_length=8)),
                ('article', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('article', models.CharField(max_length=150)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_reply', to='posts.reply')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

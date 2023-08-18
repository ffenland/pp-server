# Generated by Django 4.2.4 on 2023-08-17 14:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pharmacies', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cf_id', models.URLField()),
                ('description', models.CharField(max_length=140)),
                ('pharmacy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacies.pharmacy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

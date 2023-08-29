# Generated by Django 4.2.4 on 2023-08-29 18:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(choices=[('cash', '현금매출'), ('card', '카드매출'), ('prepare', '조제료'), ('income', '입금액')])),
                ('ammount', models.PositiveIntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('reg_number', models.CharField(blank=True, max_length=10, null=True)),
                ('address_road', models.CharField(max_length=30)),
                ('address_detail', models.CharField(max_length=30)),
                ('address_sgg_code', models.CharField(max_length=5)),
                ('address_sido', models.CharField(max_length=10)),
                ('address_sgg', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Pharmacies',
            },
        ),
    ]

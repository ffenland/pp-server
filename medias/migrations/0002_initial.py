# Generated by Django 4.2.4 on 2023-08-29 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medias', '0001_initial'),
        ('pharmacies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='pharmacy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacies.pharmacy'),
        ),
    ]

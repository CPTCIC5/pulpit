# Generated by Django 5.1.6 on 2025-03-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]

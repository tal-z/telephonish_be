# Generated by Django 4.2 on 2023-05-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_room_dramatic_reading_round_room_drawing_round_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

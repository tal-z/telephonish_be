# Generated by Django 4.2 on 2023-05-27 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_player_unique_spectator_name_in_room_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('dataUrl', models.TextField()),
                ('prompt', models.TextField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.room')),
            ],
        ),
    ]

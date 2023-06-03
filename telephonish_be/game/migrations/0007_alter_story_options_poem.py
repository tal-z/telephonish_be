# Generated by Django 4.2 on 2023-05-29 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_story'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name': 'story', 'verbose_name_plural': 'stories'},
        ),
        migrations.CreateModel(
            name='Poem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('poem', models.TextField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.room')),
            ],
        ),
    ]

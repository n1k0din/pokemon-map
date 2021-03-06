# Generated by Django 3.1.11 on 2021-05-14 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20210514_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='prev_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolution', to='pokemon_entities.pokemon'),
        ),
    ]

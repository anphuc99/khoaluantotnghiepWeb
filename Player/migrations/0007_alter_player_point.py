# Generated by Django 4.0.4 on 2022-11-17 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Player', '0006_rename_multiplier_player_point_alter_player_jump_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='point',
            field=models.IntegerField(default=1),
        ),
    ]

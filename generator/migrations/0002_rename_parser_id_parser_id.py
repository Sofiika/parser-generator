# Generated by Django 4.0.2 on 2022-05-10 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parser',
            old_name='parser_id',
            new_name='id',
        ),
    ]

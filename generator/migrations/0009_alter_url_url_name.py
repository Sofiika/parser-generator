# Generated by Django 4.0.2 on 2022-05-14 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0008_alter_xpath_xpath_class_alter_xpath_xpath_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url_name',
            field=models.TextField(help_text='Website to parse'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-05-12 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0005_alter_xpath_xpath_additions_alter_xpath_xpath_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xpath',
            name='manual',
        ),
    ]

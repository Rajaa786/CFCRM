# Generated by Django 4.0.3 on 2022-10-14 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_housewifedetails_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housewifedetails',
            name='country',
        ),
        migrations.RemoveField(
            model_name='retireddetails',
            name='country',
        ),
        migrations.RemoveField(
            model_name='studentdetails',
            name='country',
        ),
    ]

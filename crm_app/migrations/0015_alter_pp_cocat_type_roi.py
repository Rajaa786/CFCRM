# Generated by Django 4.0.5 on 2022-06-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0014_pp_cocat_type_roi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pp_cocat_type',
            name='roi',
            field=models.BigIntegerField(),
        ),
    ]

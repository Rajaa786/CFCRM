# Generated by Django 2.2.7 on 2020-10-30 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0007_profee_rdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profee',
            name='rdate',
            field=models.CharField(max_length=1000),
        ),
    ]

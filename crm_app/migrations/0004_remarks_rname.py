# Generated by Django 2.2.7 on 2020-10-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='remarks',
            name='rname',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]

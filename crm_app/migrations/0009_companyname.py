# Generated by Django 2.2.7 on 2020-10-30 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0008_auto_20201030_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='companyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compName', models.CharField(max_length=1000)),
            ],
        ),
    ]

# Generated by Django 2.2.7 on 2020-10-30 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20201024_2132'),
        ('crm_app', '0004_remarks_rname'),
    ]

    operations = [
        migrations.CreateModel(
            name='profee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=1000)),
                ('pro', models.BigIntegerField(max_length=100)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.uploads')),
            ],
        ),
    ]

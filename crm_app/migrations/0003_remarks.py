# Generated by Django 2.2.7 on 2020-10-25 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20201024_2132'),
        ('crm_app', '0002_auto_20201020_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='remarks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rdate', models.CharField(max_length=50)),
                ('rem', models.CharField(max_length=3000)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.uploads')),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2022-10-07 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
        ('HomeLoan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cibil',
            name='cibil_loan_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.cibilloantype'),
        ),
    ]

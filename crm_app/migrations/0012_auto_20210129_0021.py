# Generated by Django 3.1.4 on 2021-01-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0011_auto_20210129_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pp_cibil',
            name='effec_date4',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_cocat_type',
            name='effec_date6',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_company_type',
            name='effec_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_max_age',
            name='effec_date3',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_residence_type',
            name='effec_date2',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_salary_type',
            name='effec_date1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pp_tenure',
            name='effec_date5',
            field=models.CharField(max_length=100),
        ),
    ]

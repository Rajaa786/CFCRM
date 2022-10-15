from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.


class uploads(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    loan_type = models.CharField(max_length=100)
    custo_type = models.CharField(max_length=100)
    tenure = models.IntegerField()
    cibil_score = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=200)
    gross_sal = models.CharField(max_length=15)
    net_sal = models.CharField(max_length=15)
    age = models.CharField(max_length=50)
    retire_age = models.CharField(max_length=50)
    company_type = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    paid_up_cap = models.CharField(max_length=50)
    company_yrs = models.CharField(max_length=50)
    nature_company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    designation_type = models.CharField(max_length=200)
    current_exp = models.CharField(max_length=50)
    total_exp = models.CharField(max_length=50)
    emp_type = models.CharField(max_length=200)
    form_16 = models.CharField(max_length=200)
    residence_type = models.CharField(max_length=200)
    stt = models.CharField(max_length=200)
    sttt = models.CharField(max_length=200)
    loan_amt = models.BigIntegerField()
    criteria = models.CharField(max_length=300)
    remark = models.CharField(max_length=900)
    date = models.CharField(max_length=100)


class loan_details(models.Model):
    uid = models.ForeignKey(
        uploads, on_delete=models.CASCADE, related_name='loan_details')
    bank = models.CharField(max_length=500, blank=True, null=True)
    product = models.CharField(max_length=500, blank=True, null=True)
    loan = models.CharField(max_length=500, blank=True, null=True)
    emi = models.CharField(max_length=500, blank=True, null=True)
    roi = models.CharField(max_length=500, blank=True, null=True)
    emi_start = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    emi_end = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    bounces = models.CharField(max_length=500, blank=True, null=True)
    moratorium = models.CharField(max_length=500, blank=True, null=True)


class credit_details(models.Model):
    uid = models.ForeignKey(
        uploads, on_delete=models.CASCADE, related_name='credit_details')
    bank = models.CharField(max_length=500, blank=True, null=True)
    credit_limit = models.CharField(max_length=500, blank=True, null=True)
    limit_utilize = models.CharField(max_length=500, blank=True, null=True)
    card_age = models.CharField(max_length=500, blank=True, null=True)
    payment_delay = models.CharField(max_length=500, blank=True, null=True)
    moratorium = models.CharField(max_length=500, blank=True, null=True)

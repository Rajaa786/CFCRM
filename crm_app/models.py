from django.db import models
from customer.models import uploads

# Create your models here.


class customer_type(models.Model):
    type = models.CharField(max_length=200)


class product_policy(models.Model):
    cust_type = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    co_category = models.CharField(max_length=200)
    loan_co_category = models.CharField(max_length=200)
    gross_salary = models.CharField(max_length=200)
    net_salary = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=200)
    salary_acc = models.CharField(max_length=200)
    salary_type = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    min_age = models.CharField(max_length=200)
    max_age = models.CharField(max_length=200)
    current_exp = models.CharField(max_length=200)
    total_exp = models.CharField(max_length=200)
    cibil = models.CharField(max_length=200)
    tenure = models.CharField(max_length=200)
    res_type = models.CharField(max_length=200, null=True)


class product_and_policy(models.Model):
    cust_type = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    salary_acc = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    current_exp = models.IntegerField(null=True)
    cibil_scroe = models.IntegerField(null=True)
    roi_from = models.FloatField(null=True)
    roi_to = models.FloatField(null=True)
    effective_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    ineffective_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    cocat_type = models.ManyToManyField('cocat_type')
    company_type = models.ManyToManyField('company_type')
    salary_type = models.ManyToManyField('salary_type')
    residence_type = models.ManyToManyField('residence_type')
    tenure = models.ManyToManyField('tenure')


class tenure(models.Model):
    tenure = models.IntegerField()


class loan_type(models.Model):
    loan_type = models.CharField(max_length=200)


class bank_name(models.Model):
    b_name = models.CharField(max_length=200)


class cocat_type(models.Model):
    c_type = models.CharField(max_length=200)


class company_type(models.Model):
    co_type = models.CharField(max_length=200)


class salary_type(models.Model):
    s_type = models.CharField(max_length=200)


class residence_type(models.Model):
    r_type = models.CharField(max_length=200)


class designation(models.Model):
    design = models.CharField(max_length=200)


class bank_cat(models.Model):
    bank_name = models.CharField(max_length=200)
    co_name = models.CharField(max_length=200)
    cat = models.CharField(max_length=200)
    eff = models.CharField(max_length=50)
    ineff = models.CharField(max_length=50, null=True)


# ----------------------------------------------------- TRIAL ------------------------------------------------

class prod_policy_master(models.Model):
    pp_id = models.BigIntegerField()
    prod_name = models.CharField(max_length=200)
    bank_names = models.CharField(max_length=200)
    type_of_cust = models.CharField(max_length=200)
    salary_acc = models.CharField(max_length=100)
    salary_exist = models.BigIntegerField()
    salary_new = models.BigIntegerField()
    designs = models.CharField(max_length=200)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    current_exp = models.IntegerField()
    roi = models.CharField(max_length=100)
    multiplier = models.CharField(max_length=100)
    foir = models.CharField(max_length=100)
    both = models.CharField(max_length=100)
    eff_date = models.CharField(max_length=100)
    ineff_date = models.CharField(max_length=100)
    processing_fee = models.BigIntegerField()
    #months = models.BigIntegerField()

    def __str__(self):
        s = self.bank_names[:4] + self.prod_name[:3] + self.type_of_cust[:3]
        #s = self.pp_id
        return s.upper()


class pp_company_type(models.Model):
    ppid = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='comptypes')
    comp_type = models.CharField(max_length=200)


class pp_salary_type(models.Model):
    ppid1 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='saltypes')
    sal_type = models.CharField(max_length=200)


class pp_residence_type(models.Model):
    ppid2 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='restypes')
    res_type = models.CharField(max_length=200)


class pp_max_age(models.Model):
    ppid3 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='maxages')
    max_type = models.IntegerField()


class pp_cibil(models.Model):
    ppid4 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='mincibil')
    cibil_type = models.IntegerField()


class pp_tenure(models.Model):
    ppid5 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='tenures')
    ten_type = models.IntegerField()


class pp_cocat_type(models.Model):
    ppid6 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='cocattypes')
    cocat_types = models.CharField(max_length=200)
    cocat_no = models.IntegerField()
    roi = models.FloatField()
    min_loan_amt = models.BigIntegerField()
    max_loan_amt = models.BigIntegerField()


class pp_foir(models.Model):
    ppid7 = models.ForeignKey(
        prod_policy_master, on_delete=models.CASCADE, related_name='foirs')
    min_amt = models.BigIntegerField()
    max_amt = models.BigIntegerField()
    cutoff = models.IntegerField()


class reasons(models.Model):
    rname = models.CharField(max_length=300)
    rrea = models.CharField(max_length=300)


class remarks(models.Model):
    uid = models.ForeignKey(uploads, on_delete=models.CASCADE)
    rname = models.CharField(max_length=1000)
    rdate = models.CharField(max_length=50)
    rem = models.CharField(max_length=3000)


class profee(models.Model):
    uid = models.ForeignKey(uploads, on_delete=models.CASCADE)
    cname = models.CharField(max_length=1000)
    pro = models.BigIntegerField()
    rdate = models.CharField(max_length=1000)


class companyName(models.Model):
    compName = models.CharField(max_length=1000)

from django.shortcuts import render, redirect
from customer.models import uploads, loan_details, credit_details
from .models import customer_type, bank_name, cocat_type, company_type, salary_type, residence_type, designation, \
    product_policy
from .models import loan_type, bank_cat, tenure, product_and_policy
from .models import prod_policy_master, pp_company_type, pp_salary_type, pp_residence_type
from .models import pp_cibil, pp_tenure, pp_cocat_type, reasons, pp_foir, remarks, profee, companyName
from datetime import datetime, date
# import datetime
import smtplib
import pywhatkit
from django.contrib.auth.models import User, auth
import csv
import io
from .resources import ImportsResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from collections import Counter
from django.core.mail import EmailMultiAlternatives
from leadgenerator.settings import EMAIL_HOST_USER
import time
import webbrowser as web
import pyautogui as pg


# Create your views here.

def not_listed(request):
    a = uploads.objects.all()
    l = []
    for i in a:
        if (i.paid_up_cap != '') or (i.company_yrs != '') or (i.nature_company != ''):
            s = uploads.objects.get(id=i.id)
            l.append(s)
    return render(request, 'not_listed.html', {'alldata': l})


def dash(request):
    return render(request, 'crm_dashboard.html')


def log(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        passw = request.POST.get('passw')

        user = auth.authenticate(username=user, password=passw)

        if user is not None:
            auth.login(request, user)
            return redirect('/crm_app/customer')

        else:
            return render(request, 'login.html')


def customer(request):
    a = uploads.objects.all()
    return render(request, 'crm_customer.html', {'alldata': a})


def logout(request):
    auth.logout(request)
    return redirect('/crm_app/log')


def master_cust_type(request):
    a = customer_type.objects.all()
    return render(request, 'master_cust_type.html', {'alldata': a})


def add_cust_type(request):
    return render(request, 'add_cust_type.html')


def add_prd_ply(request):
    cust_type = customer_type.objects.all()
    l_type = loan_type.objects.all()
    bank = bank_name.objects.all()
    s_type = salary_type.objects.all()
    res_type = residence_type.objects.all()
    des_type = designation.objects.all()
    com_type = company_type.objects.all()
    cocatt_type = cocat_type.objects.all()
    tenures = tenure.objects.all()

    return render(request, 'add_prd_ply.html',
                  {'cust_type': cust_type, 'l_type': l_type, 'bank': bank, 's_type': s_type, 'res_type': res_type,
                   'des_type': des_type, 'com_type': com_type, 'cocatt_type': cocatt_type, 'tenures': tenures})


def prd_ply_edit(request, id):
    prd = product_policy.objects.get(id=id)
    cust_type = customer_type.objects.all()
    l_type = loan_type.objects.all()
    bank = bank_name.objects.all()
    s_type = salary_type.objects.all()
    res_type = residence_type.objects.all()
    des_type = designation.objects.all()
    com_type = company_type.objects.all()
    return render(request, 'prd_ply_edit.html',
                  {'prd': prd, 'cust_type': cust_type, 'l_type': l_type, 'bank': bank, 's_type': s_type,
                   'res_type': res_type, 'des_type': des_type, 'com_type': com_type})


def load_company(request):
    bank_name = request.GET.get('bank')
    companies = bank_cat.objects.filter(bank_name=bank_name)

    return render(request, 'company_dropdown.html', {'companies': companies})


def load_cocat(request):
    co_name = request.GET.get('company')
    cocats = bank_cat.objects.filter(co_name=co_name)

    return render(request, 'cocat_dropdown.html', {'cocats': cocats})


def add_cust_type_table(request):
    if request.method == 'POST':
        cust_type = request.POST.get('cust_type')
        o = customer_type(type=cust_type)
        o.save()
        # pyautogui.alert("Upload Done")
    a = customer_type.objects.all()
    return render(request, 'master_cust_type.html', {'alldata': a})


def master_loan_type(request):
    a = loan_type.objects.all()
    return render(request, 'master_loan_type.html', {'alldata': a})


def add_loan_type(request):
    return render(request, 'add_loan_type.html')


def add_loan_type_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = loan_type(loan_type=type)
        o.save()
        # pyautogui.alert("Upload Done")
    a = loan_type.objects.all()
    return render(request, 'master_loan_type.html', {'alldata': a})


def master_bank_name(request):
    a = bank_name.objects.all()
    return render(request, 'master_bank_name.html', {'alldata': a})


def add_bank_name(request):
    return render(request, 'add_bank_name.html')


def add_prd_ply_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            loan_type = request.POST.get('loan_type')
            bank_name = request.POST.get('bank_name')
            company_name = request.POST.get('company_name')
            cocat_type = request.POST.get('cocat_type')
            loan_co_category = request.POST.get('loan_cocat')
            gross_salary = request.POST.get('gross_salary')
            net_salary = request.POST.get('net_salary')
            company_type = request.POST.get('company_type')
            salary_acc = request.POST.get('salary_acc')
            salary_type = request.POST.get('salary_type')
            res_type = request.POST.get('res_type')
            designation = request.POST.get('designation')
            min_age = request.POST.get('min_age')
            max_age = request.POST.get('max_age')
            current_exp = request.POST.get('current_exp')
            total_exp = request.POST.get('total_exp')
            cibil_score = request.POST.get('cibil_score')
            tenure = request.POST.get('tenure')
            pf = request.POST.get('pf')
            mon = request.POST.get('mon')
            abc = product_policy(cust_type=cust_type, loan_type=loan_type, bank_name=bank_name,
                                 co_category=cocat_type, company_name=company_name, salary_type=salary_type,
                                 designation=designation, min_age=min_age, max_age=max_age, current_exp=current_exp,
                                 total_exp=total_exp, cibil=cibil_score, tenure=tenure,
                                 loan_co_category=loan_co_category,
                                 gross_salary=gross_salary,
                                 net_salary=net_salary, salary_acc=salary_acc, res_type=res_type,
                                 company_type=company_type,
                                 processing_fee=2000, months=6
                                 )
            abc.save()

        return redirect('crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def add_prd_ply_table1(request):
    cust_type = request.POST.get('cust_type')
    loan_type = request.POST.get('loan_type')
    bank_name = request.POST.get('bank_name')
    salary_acc = request.POST.get('salary_acc')
    designation = request.POST.get('designation')
    min_age = request.POST.get('min_age')
    max_age = request.POST.get('max_age')
    current_exp = request.POST.get('current_exp')
    cibil_score = request.POST.get('cibil_score')
    roi_from = request.POST.get('min_roi')
    roi_to = request.POST.get('max_roi')
    effective_date = request.POST.get('effective_date')
    ineffective_date = request.POST.get('ineffective_date')
    cocat_type_ = request.POST.getlist('cocat_type')
    co_type = request.POST.getlist('company_type')
    salary_type_ = request.POST.getlist('salary_type')
    res_type_ = request.POST.getlist('res_type')
    tenure_ = request.POST.getlist('tenure')

    abc = product_and_policy.objects.create(cust_type=cust_type, loan_type=loan_type, bank_name=bank_name,
                                            salary_acc=salary_acc, designation=designation, min_age=min_age,
                                            max_age=max_age, current_exp=current_exp, cibil_scroe=cibil_score,
                                            roi_from=roi_from, roi_to=roi_to, effective_date=effective_date,
                                            ineffective_date=ineffective_date)

    for i in cocat_type_:
        abcd = cocat_type.objects.filter(c_type=i).values('id')
        abc.cocat_type.add(abcd)

    for i in co_type:
        abcd = company_type.objects.filter(co_type=i).values('id')
        abc.company_type.add(abcd)

    for i in salary_type_:
        abcd = salary_type.objects.filter(s_type=i).values('id')
        abc.salary_type.add(abcd)

    for i in res_type_:
        abcd = residence_type.objects.filter(r_type=i).values('id')
        abc.residence_type.add(abcd)

    for i in tenure_:
        abcd = tenure.objects.filter(tenure=i).values('id')
        abc.tenure.add(abcd)

    return redirect('crm_app/master_product_policy')


def add_prod_policy_table(request):
    if request.method == "POST":
        cust_type = request.POST.get('cust_type')
        loan_type = request.POST.get('loan_type')
        bank_name = request.POST.get('bank_name')
        salary_acc = request.POST.get('salary_acc')
        designation = request.POST.get('designation')
        min_age = request.POST.get('min_age')
        max_age = request.POST.get('max_age')
        current_exp = request.POST.get('current_exp')
        cibil_score = request.POST.getlist('cibil_score')

        roi = request.POST.getlist('roi')
        roi = int(roi)
        if roi > 40:
            roi = roi / 100
        effective_date = str(datetime.now())[:22]
        cocat_type_ = request.POST.getlist('cocat_type')
        min_loan_amount = request.POST.getlist('min_loan_amt')
        max_loan_amount = request.POST.getlist('max_loan_amt')
        co_type = request.POST.getlist('company_type')
        min_net_sal = request.POST.getlist('min_net_sal')
        max_net_sal = request.POST.getlist('max_net_sal')
        cutoff = request.POST.getlist('cutoff')
        salary_type_ = request.POST.getlist('salary_type')
        res_type_ = request.POST.getlist('res_type')
        tenure_ = request.POST.getlist('tenure')
        cocat_no_ = request.POST.getlist('cocat_no')
        salary_exist = request.POST.get('salary_exist')
        salary_new = request.POST.get('salary_new')
        mon = request.POST.get('mon')
        pf = request.POST.get('pf')
        try:
            obj = prod_policy_master.objects.latest('id')
            pp_id = obj.id + 1
        except prod_policy_master.DoesNotExist:
            pp_id = 1

        abc = prod_policy_master(id=pp_id, prod_name=loan_type, bank_names=bank_name, type_of_cust=cust_type,
                                 salary_acc=salary_acc, salary_exist=salary_exist, salary_new=salary_new,
                                 designs=designation, min_age=min_age, max_age=max_age, current_exp=current_exp,
                                 eff_date=effective_date, ineff_date='', pp_id=pp_id,
                                 multiplier='', foir='', both='yes', processing_fee=pf, months=mon)

        abc.save()

        for i in co_type:
            abc = pp_company_type(comp_type=i, ppid_id=pp_id)
            abc.save()

        for (i, j, k, l, m) in zip(cocat_type_, min_loan_amount, max_loan_amount, cocat_no_, roi):
            abc = pp_cocat_type(cocat_no=l, cocat_types=i, min_loan_amt=j, max_loan_amt=k, roi=m,
                                ppid6_id=pp_id)
            abc.save()

        for (x, y, z) in zip(min_net_sal, max_net_sal, cutoff):
            abc = pp_foir(ppid7_id=pp_id, min_amt=x, max_amt=y, cutoff=z)
            abc.save()

        for i in res_type_:
            abc = pp_residence_type(res_type=i, ppid2_id=pp_id)
            abc.save()

        for i in salary_type_:
            abc = pp_salary_type(sal_type=i, ppid1_id=pp_id)
            abc.save()

        for i in tenure_:
            abc = pp_tenure(ten_type=i, ppid5_id=pp_id)
            abc.save()

        for i in cibil_score:
            abc = pp_cibil(cibil_type=i, ppid4_id=pp_id)
            abc.save()

        return redirect('/crm_app/master_product_policy')


def prd_ply_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            loan_type = request.POST.get('loan_type')
            bank_name = request.POST.get('bank_name')
            company_name = request.POST.get('company_name')
            cocat_type = request.POST.get('cocat_type')
            loan_co_category = request.POST.get('loan_cocat')
            gross_salary = request.POST.get('gross_salary')
            net_salary = request.POST.get('net_salary')
            company_type = request.POST.get('company_type')
            salary_acc = request.POST.get('salary_acc')
            salary_type = request.POST.get('salary_type')
            res_type = request.POST.get('res_type')
            designation = request.POST.get('designation')
            min_age = request.POST.get('min_age')
            max_age = request.POST.get('max_age')
            current_exp = request.POST.get('current_exp')
            total_exp = request.POST.get('total_exp')
            cibil_score = request.POST.get('cibil_score')
            tenure = request.POST.get('tenure')
            pid = request.POST.get('id')

            abc = product_policy.objects.get(id=pid)
            abc.cust_type = cust_type
            abc.bank_name = bank_name
            abc.co_category = cocat_type
            abc.company_name = company_name
            abc.salary_type = salary_type
            abc.designation = designation
            abc.min_age = min_age
            abc.max_age = max_age
            abc.current_exp = current_exp
            abc.total_exp = total_exp
            abc.cibil = cibil_score
            abc.tenure = tenure
            abc.loan_co_category = loan_co_category
            abc.gross_salary = gross_salary
            abc.net_salary = net_salary
            abc.salary_acc = salary_acc
            abc.res_type = res_type
            abc.company_type = company_type
            abc.save()

        a = product_policy.objects.all()
        return redirect('crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def add_bank_name_table(request):
    if request.method == 'POST':
        name = request.POST.get('bank_name')
        o = bank_name(b_name=name)
        o.save()
        # pyautogui.alert("Upload Done")
    a = bank_name.objects.all()
    return render(request, 'master_bank_name.html', {'alldata': a})


def master_cocat_type(request):
    a = pp_cocat_type.objects.all()
    return render(request, 'master_cocat_type.html', {'alldata': a})


def add_cocat_type(request):
    a = prod_policy_master.objects.all()
    s = cocat_type.objects.all()
    return render(request, 'add_cocat_type.html', {'a': a, 's': s})


def add_cocat_type_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        cocat_types = request.POST.get('cocat_types')
        cocat_no = request.POST.get('cocat_no')
        roi = request.POST.get('roi')
        roi = int(roi)
        if roi > 40:
            roi = roi / 100
        min_loan_amt = request.POST.get('min_loan_amt')
        max_loan_amt = request.POST.get('max_loan_amt')
        o = pp_cocat_type(ppid6=sid, cocat_types=cocat_types, cocat_no=cocat_no, min_loan_amt=min_loan_amt,
                          max_loan_amt=max_loan_amt, roi=roi)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def master_company_type(request):
    a = pp_company_type.objects.all()
    return render(request, 'master_company_type.html', {'alldata': a})


def add_company_type(request):
    a = prod_policy_master.objects.all()
    s = company_type.objects.all()
    return render(request, 'add_company_type.html', {'a': a, 's': s})


def add_company_type_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        m = request.POST.get('m')
        o = pp_company_type(ppid=sid, comp_type=m)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def master_salary_type(request):
    a = pp_salary_type.objects.all()
    return render(request, 'master_salary_type.html', {'alldata': a})


def add_salary_type(request):
    a = prod_policy_master.objects.all()
    s = salary_type.objects.all()
    return render(request, 'add_salary_type.html', {'a': a, 's': s})


def add_salary_type_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        m = request.POST.get('m')
        o = pp_salary_type(ppid1=sid, sal_type=m)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def add_residence_type(request):
    a = prod_policy_master.objects.all()
    s = residence_type.objects.all()
    return render(request, 'add_residence_type.html', {'a': a, 's': s})


def add_residence_type_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        m = request.POST.get('m')
        o = pp_residence_type(ppid2=sid, res_type=m)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def master_designation(request):
    a = designation.objects.all()
    return render(request, 'master_designation.html', {'alldata': a})


def add_designation(request):
    return render(request, 'add_designation.html')


def add_designation_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = designation(design=type)
        o.save()
        # pyautogui.alert("Upload Done")
    a = designation.objects.all()
    return render(request, 'master_designation.html', {'alldata': a})


def master_bank_cat(request):
    a = bank_cat.objects.all()
    return render(request, 'master_bank_cat.html', {'alldata': a})


def add_bank_cat(request):
    a = cocat_type.objects.all()
    b = bank_name.objects.all()
    c = companyName.objects.all()
    return render(request, 'add_bank_cat.html', {'cname': a, 'bname': b, 'c': c})


def bank_cat_delete(request, id):
    m = bank_cat.objects.get(pk=id).delete()
    return redirect('/crm_app/master_bank_cat')


def add_bank_cat_table(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        co_name = request.POST.get('co_name')
        cat = request.POST.get('cat')
        now = str(datetime.now())
        eff = now[:22]
        ineff = ''
        o = bank_cat(bank_name=bank_name, co_name=co_name, cat=cat, eff=eff, ineff=ineff)
        o.save()
        # pyautogui.alert("Upload Done")
    a = bank_cat.objects.all()
    return render(request, 'master_bank_cat.html', {'alldata': a})


#                                                -------------------------------------------
# Customer Type Start

def cust_type_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            pid = request.POST.get('id')

            abc = customer_type.objects.get(id=pid)
            abc.type = cust_type
            abc.save()

        a = customer_type.objects.all()
        return redirect('crm_app/master_cust_type')
    except:
        return render(request, 'failure.html')


def cust_type_edit(request, id):
    cust = customer_type.objects.get(id=id)
    cust_type = customer_type.objects.all()
    return render(request, 'cust_type_edit.html', {'prd': cust, 'cust_type': cust_type})


# Customer Type End
#                                                -------------------------------------------

#                                                -------------------------------------------
# Loan Type Start

def loan_type_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            pid = request.POST.get('id')

            abc = loan_type.objects.get(id=pid)
            abc.loan_type = cust_type
            abc.save()

        a = loan_type.objects.all()
        return redirect('crm_app/master_loan_type')
    except:
        return render(request, 'failure.html')


def loan_type_edit(request, id):
    cust = loan_type.objects.get(id=id)
    cust_type = loan_type.objects.all()
    return render(request, 'loan_type_edit.html', {'prd': cust, 'cust_type': cust_type})


# Loan Type End
#                                                -------------------------------------------

#                                                -------------------------------------------
# Bank Name Start

def bank_name_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            pid = request.POST.get('id')

            abc = bank_name.objects.get(id=pid)
            abc.b_name = cust_type
            abc.save()

        a = bank_name.objects.all()
        return redirect('crm_app/master_bank_name')
    except:
        return render(request, 'failure.html')


def bank_name_edit(request, id):
    cust = bank_name.objects.get(id=id)
    cust_type = bank_name.objects.all()
    return render(request, 'bank_name_edit.html', {'prd': cust, 'cust_type': cust_type})


# Bank Name End
#                                                -------------------------------------------

#                                                -------------------------------------------
# Co-Category Type Start

def cocat_type_edit_table(request):
    try:
        if request.method == 'POST':
            cocat_type = request.POST.get('cocat_type')
            min_amt = request.POST.get('min_amt')
            max_amt = request.POST.get('max_amt')
            pid = request.POST.get('id')
            cocat_no = request.POST.get('cocat_no')
            roi = request.POST.get('roi')
            roi = int(roi)
            if roi > 40:
                roi = roi / 100
            print(roi)
            abc = pp_cocat_type.objects.get(id=pid)
            abc.cocat_types = cocat_type
            abc.cocat_no = cocat_no
            abc.roi = roi
            abc.min_loan_amt = min_amt
            abc.max_loan_amt = max_amt
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def cocat_type_edit(request, id):
    m = pp_cocat_type.objects.get(id=id)
    return render(request, 'cocat_type_edit.html', {'prd': m})


def cocat_type_delete(request, id):
    m = pp_cocat_type.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Co-Category Type End
#

#                                                -------------------------------------------
# Bank-Category Type Start

def bank_cat_edit_table(request):
    try:
        if request.method == 'POST':
            comp_name = request.POST.get('comp_name')
            pid = request.POST.get('id')
            abc = bank_cat.objects.get(id=pid)
            abc.cat = comp_name
            abc.save()

        a = bank_cat.objects.all()
        return redirect(master_bank_cat)
    except:
        return render(request, 'failure.html')


def bank_cat_edit(request, id):
    m = bank_cat.objects.get(id=id)
    cust_type = bank_cat.objects.all()
    bank = bank_name.objects.all()
    cate = cocat_type.objects.all()
    return render(request, 'bank_cat_edit.html', {'prd': m, 'cust_type': cust_type, 'bank': bank, 'cate': cate})


# Bank-Category Type End
#

#                                                -------------------------------------------
# Company Type Start

def company_type_edit_table(request):
    try:
        if request.method == 'POST':
            comp_type = request.POST.get('comp_type')
            pid = request.POST.get('id')
            abc = pp_company_type.objects.get(id=pid)
            abc.comp_type = comp_type
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def company_type_edit(request, id):
    m = pp_company_type.objects.get(id=id)
    cust_type = company_type.objects.all()
    return render(request, 'company_type_edit.html', {'prd': m, 'cust_type': cust_type})


def company_type_delete(request, id):
    m = pp_company_type.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Company Type End
#

#                                                -------------------------------------------
# Salary Type Start

def salary_type_edit_table(request):
    try:
        if request.method == 'POST':
            sal_type = request.POST.get('sal_type')
            pid = request.POST.get('id')

            abc = pp_salary_type.objects.get(id=pid)
            abc.sal_type = sal_type
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def salary_type_edit(request, id):
    m = pp_salary_type.objects.get(id=id)
    cust_type = pp_salary_type.objects.all()
    return render(request, 'salary_type_edit.html', {'prd': m, 'cust_type': cust_type})


def salary_type_delete(request, id):
    m = pp_salary_type.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Salary Type End
#

#                                                -------------------------------------------
# Residence Type Start

def master_residence_type(request):
    a = pp_residence_type.objects.all()
    return render(request, 'master_residence_type.html', {'alldata': a})


def residence_type_edit_table(request):
    try:
        if request.method == 'POST':
            res_type = request.POST.get('res_type')
            pid = request.POST.get('id')
            abc = pp_residence_type.objects.get(id=pid)
            abc.res_type = res_type
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def residence_type_edit(request, id):
    m = pp_residence_type.objects.get(id=id)
    cust_type = residence_type.objects.all()
    return render(request, 'residence_type_edit.html', {'prd': m, 'cust_type': cust_type})


def residence_type_delete(request, id):
    m = pp_residence_type.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Residence Type End
#

#                                                -------------------------------------------
# Designation Type Start

def designation_type_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            pid = request.POST.get('id')

            abc = designation.objects.get(id=pid)
            abc.design = cust_type
            abc.save()

        a = designation.objects.all()
        return redirect('crm_app/master_designation')
    except:
        return render(request, 'failure.html')


def designation_type_edit(request, id):
    cust = designation.objects.get(id=id)
    cust_type = designation.objects.all()
    return render(request, 'designation_type_edit.html', {'prd': cust, 'cust_type': cust_type})


# Designation Type End
#

#                                                -------------------------------------------
# Cibil Start

def master_cibil(request):
    a = pp_cibil.objects.all()
    return render(request, 'master_cibil.html', {'alldata': a})


def cibil_edit_table(request):
    try:
        if request.method == 'POST':
            cibil_type = request.POST.get('cibil_type')
            pid = request.POST.get('id')

            abc = pp_cibil.objects.get(id=pid)
            abc.cibil_type = cibil_type
            abc.save()
        return redirect(master_cibil)
    except:
        return render(request, 'failure.html')


def cibil_edit(request, id):
    m = pp_cibil.objects.get(id=id)
    return render(request, 'cibil_edit.html', {'prd': m})


# Cibil End
#

#                                                -------------------------------------------
# Tenure Start

def master_tenure(request):
    a = pp_tenure.objects.all()
    return render(request, 'master_tenure.html', {'alldata': a})


def tenure_edit_table(request):
    try:
        if request.method == 'POST':
            ten_type = request.POST.get('ten_type')
            pid = request.POST.get('id')

            abc = pp_tenure.objects.get(id=pid)
            abc.ten_type = ten_type
            abc.save()
        return redirect(master_tenure)
    except:
        return render(request, 'failure.html')


def tenure_edit(request, id):
    m = pp_tenure.objects.get(id=id)
    return render(request, 'tenure_edit.html', {'prd': m})


def tenure_delete(request, id):
    m = pp_tenure.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Tenure End
#


# Cibil Start

def add_cibil(request):
    a = prod_policy_master.objects.all()
    return render(request, 'add_cibil.html', {'a': a})


def add_cibil_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        cibil = request.POST.get('cibil')
        o = pp_cibil(ppid4=sid, cibil_type=cibil)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def master_cibil(request):
    a = pp_cibil.objects.all()
    return render(request, 'master_cibil.html', {'alldata': a})


def cibil_edit_table(request):
    try:
        if request.method == 'POST':
            cibil_type = request.POST.get('cibil_type')
            pid = request.POST.get('id')

            abc = pp_cibil.objects.get(id=pid)
            abc.cibil_type = cibil_type
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def cibil_edit(request, id):
    m = pp_cibil.objects.get(pk=id)
    return render(request, 'cibil_edit.html', {'prd': m})


def cibil_delete(request, id):
    m = pp_cibil.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Cibil End
#

#                                                -------------------------------------------
# Tenure Start

def add_tenure(request):
    a = prod_policy_master.objects.all()
    s = tenure.objects.all()
    return render(request, 'add_tenure.html', {'a': a, 's': s})


def add_tenure_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        ten_type = request.POST.get('ten_type')
        o = pp_tenure(ppid5=sid, ten_type=ten_type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def master_tenure(request):
    a = pp_tenure.objects.all()
    return render(request, 'master_tenure.html', {'alldata': a})


def tenure_edit_table(request):
    try:
        if request.method == 'POST':
            ten_type = request.POST.get('ten_type')
            pid = request.POST.get('id')

            abc = pp_tenure.objects.get(id=pid)
            abc.ten_type = ten_type
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def tenure_edit(request, id):
    m = pp_tenure.objects.get(id=id)
    return render(request, 'tenure_edit.html', {'prd': m})


# Tenure End
#


#                                                -------------------------------------------
# PP Start

def master_product_policy(request):
    a = prod_policy_master.objects.all()
    cocat = pp_cocat_type.objects.all()
    return render(request, 'master_product_policy.html', {'a': a, 'c': cocat})


def pp_edit_table(request):
    try:
        if request.method == 'POST':
            bank_names = request.POST.get('bank_names')
            type_of_cust = request.POST.get('type_of_cust')
            salary_acc = request.POST.get('salary_acc')
            designs = request.POST.get('designs')
            min_age = request.POST.get('min_age')
            max_age = request.POST.get('max_age')
            current_exp = request.POST.get('current_exp')
            pid = request.POST.get('id')
            abc = prod_policy_master.objects.get(id=pid)
            abc.bank_names = bank_names
            abc.type_of_cust = type_of_cust
            abc.salary_acc = salary_acc
            abc.designs = designs
            abc.min_age = min_age
            abc.max_age = max_age
            abc.current_exp = current_exp

            abc.save()
        return redirect(master_product_policy)
    except:
        return render(request, 'failure.html')


def ineff(request, id):
    abc = prod_policy_master.objects.get(id=id)
    if abc.ineff_date == '':
        abc.ineff_date = str(datetime.now())[:22]
    else:
        abc.ineff_date = ''
    abc.save()
    return redirect('/crm_app/master_product_policy')


def pp_edit(request, id):
    m = prod_policy_master.objects.get(id=id)
    cibil = pp_cibil.objects.all()
    tenure = pp_tenure.objects.all()
    cocat = pp_cocat_type.objects.all()
    company = pp_company_type.objects.all()
    salary = pp_salary_type.objects.all()
    res = pp_residence_type.objects.all()
    foir = pp_foir.objects.all()
    return render(request, 'pp_edit.html', {'prd': m, 'cibil': cibil, 'tenure': tenure, 'cocat': cocat,
                                            'company': company, 'salary': salary, 'res': res, 'foir': foir})


# PP End
#

#                                                -------------------------------------------
# PP Entire Master Start

def pp_master(request):
    a = prod_policy_master.objects.all()
    return render(request, 'pp_master.html', {'a': a})


def ppm_search(request, id):
    v = prod_policy_master.objects.get(id=id)
    c = pp_cibil.objects.all()
    cocat = pp_cocat_type.objects.all()
    comp = pp_company_type.objects.all()
    max = pp_max_age.objects.all()
    res = pp_residence_type.objects.all()
    sal = pp_salary_type.objects.all()
    ten = pp_tenure.objects.all()
    return render(request, 'ppm_search.html',
                  {'v': v, 'c': c, 'cocat': cocat, 'comp': comp, 'max': max, 'res': res, 'sal': sal, 'ten': ten})


def add_prp(request):
    return render(request, 'add_cibil.html')


# PP Entire Master End
#

#                                                -------------------------------------------
# Customer Details Start

def customer(request):
    a = uploads.objects.all()
    return render(request, 'crm_customer.html', {'alldata': a})


def cust_edit(request, id):
    v = uploads.objects.get(id=id)
    t = tenure.objects.all().distinct()
    custo_type = customer_type.objects.all().distinct()
    b = company_type.objects.all()
    c = designation.objects.all()
    loan = loan_details.objects.all()
    com = companyName.objects.all()
    loancal = 0
    creditcal = 0
    for i in loan:
        if id == i.uid_id:
            loancal = 1
    credit = credit_details.objects.all()
    for i in credit:
        if id == i.uid_id:
            creditcal = 1
    return render(request, 'cust_edit.html',
                  {'prd': v, 't': t, 'custo_type': custo_type, 'com_type': b, 'des': c, 'loan': loan, 'credit': credit,
                   'loancal': loancal, 'creditcal': creditcal, 'com': com})


def cust_view(request, id):
    v = uploads.objects.get(id=id)
    t = tenure.objects.all().distinct()
    custo_type = customer_type.objects.all().distinct()
    b = company_type.objects.all()
    c = designation.objects.all()
    loan = loan_details.objects.all()
    com = companyName.objects.all()
    loancal = 0
    creditcal = 0
    for i in loan:
        if id == i.uid_id:
            loancal = 1
    credit = credit_details.objects.all()
    for i in credit:
        if id == i.uid_id:
            creditcal = 1
    return render(request, 'cust_view.html',
                  {'prd': v, 't': t, 'custo_type': custo_type, 'com_type': b, 'des': c, 'loan': loan, 'credit': credit,
                   'loancal': loancal, 'creditcal': creditcal, 'com': com})


def cust_edit_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        cibil_score = request.POST.get('cibil_score')
        bank_name = request.POST.get('bank_name')
        gross_sal = request.POST.get('gross_sal')
        net_sal = request.POST.get('net_sal')
        age = request.POST.get('age')
        retire_age = request.POST.get('retire_age')
        company_type = request.POST.get('company_type')
        designation = request.POST.get('designation')
        designation_type = request.POST.get('designation_type')
        current_exp = request.POST.get('current_exp')
        total_exp = request.POST.get('total_exp')
        emp_type = request.POST.get('emp_type')
        form_16 = request.POST.get('form_16')
        residence_type = request.POST.get('residence_type')
        stt = request.POST.get('stt')
        sttt = request.POST.get('sttt')
        ten = request.POST.get('ten')
        # tenure = request.POST.get('tenure')
        custo_type = request.POST.get('custo_type')
        loan_type = request.POST.get('loan_type')
        pid = request.POST.get('id')
        company_name = request.POST.get('company_name')
        loan_amt = request.POST.get('loan_amt')
        abc = uploads.objects.get(id=pid)
        abc.company_name = company_name
        abc.loan_amt = loan_amt
        abc.criteria = ''
        abc.remark = ''
        abc.paid_up_cap = ''
        abc.company_yrs = ''
        abc.nature_company = ''
        abc.loan_type = loan_type
        abc.tenure = ten
        abc.custo_type = custo_type
        abc.name = name
        abc.mobile = mobile
        abc.email = email
        abc.cibil_score = cibil_score
        abc.bank_name = bank_name
        abc.gross_sal = gross_sal
        abc.net_sal = net_sal
        abc.age = age
        abc.retire_age = retire_age
        abc.company_type = company_type
        abc.designation = designation
        abc.designation_type = designation_type
        abc.current_exp = current_exp
        abc.total_exp = total_exp
        abc.emp_type = emp_type
        abc.form_16 = form_16
        abc.residence_type = residence_type
        abc.stt = stt
        abc.sttt = sttt
        abc.save()
        # pyautogui.alert("Upload Done")
    return redirect(customer)


def check_eligible(request, id):
    v = uploads.objects.get(id=id)
    c = pp_cibil.objects.all()
    comp = pp_company_type.objects.all()
    bnkcat = bank_cat.objects.all()
    ten = pp_tenure.objects.all()
    pc = pp_cocat_type.objects.all()
    rs = pp_residence_type.objects.all()
    rea = reasons.objects.all()
    l = []
    msg = ''
    camt = 0
    cat = 'Not calculated'
    elamt = 0
    alamt = 0
    cv = ''
    prod = ''
    final = 0
    alamt1 = 0
    eligible = 0
    cate = ''
    mul = 0
    foi = 0
    for i in c:
        prod = prod_policy_master.objects.get(id=i.ppid4_id)
        if v.loan_type == prod.prod_name:
            if v.custo_type == prod.type_of_cust:
                if int(v.cibil_score) >= i.cibil_type:
                    if (int(v.age) >= prod.min_age) and (int(v.age) < prod.max_age):
                        for j in comp:
                            if i.ppid4 == j.ppid:
                                if v.company_type == j.comp_type:
                                    for k in bnkcat:
                                        if prod.bank_names == k.bank_name:
                                            if v.company_name == k.co_name:
                                                for a in pc:
                                                    if i.ppid4 == a.ppid6:
                                                        if k.cat == a.cocat_types:
                                                            cat = k.cat
                                                            elamt = int(v.net_sal) * (a.cocat_no)
                                                            co = a.cocat_no
                                                            if elamt > a.max_loan_amt:
                                                                alamt = a.max_loan_amt
                                                                final = alamt
                                                                camt = a.max_loan_amt
                                                            else:
                                                                alamt = elamt
                                                                final = alamt
                                                                camt = a.max_loan_amt
                                                        for m in rs:
                                                            if m.ppid2 == i.ppid4:
                                                                if v.residence_type == m.res_type:
                                                                    if int(v.total_exp) >= prod.current_exp:
                                                                        for t in ten:
                                                                            if i.ppid4 == t.ppid5:
                                                                                if v.tenure == t.ten_type:
                                                                                    if int(v.net_sal) >= int(
                                                                                            prod.salary_new):
                                                                                        # l1=[]
                                                                                        # l1.append(prod.pp_id)
                                                                                        # l1.append(alamt)
                                                                                        # l1.append(elamt)
                                                                                        # l.append()

                                                                                        if alamt > v.loan_amt:
                                                                                            mul = v.loan_amt
                                                                                        else:
                                                                                            mul = alamt
                                                                                        cate = cat
                                                                                        l.append(prod.pp_id)
                                                                                        msg = 'ELIGIBLE'
                                                                    else:
                                                                        if msg != 'ELIGIBLE':
                                                                            for mno in rea:
                                                                                if mno.rname == 'total experience':
                                                                                    msg = mno.rrea
                                                                else:
                                                                    if msg != 'ELIGIBLE':
                                                                        for mno in rea:
                                                                            if mno.rname == 'Residence Type':
                                                                                msg = mno.rrea
                    else:
                        if msg != 'ELIGIBLE':
                            for mno in rea:
                                if mno.rname == 'age':
                                    msg = mno.rrea
                else:
                    if msg != 'ELIGIBLE':
                        for mno in rea:
                            if mno.rname == 'cibil score':
                                msg = mno.rrea

    if msg != 'ELIGIBLE':
        if msg == '':
            msg = 'Other criteria is not satisfying'

    sets = set(l)
    cv = list(sets)
    prod = prod_policy_master.objects.all()
    loan = loan_details.objects.all()
    credit = credit_details.objects.all()
    cut = 0
    f = pp_foir.objects.all()
    for i in f:
        if (int(v.net_sal) > i.min_amt) and (int(v.net_sal) <= i.max_amt):
            cut = int(v.net_sal) * i.cutoff / 100
    sum_limit = 0
    ob = 0
    for i in credit:
        if v.id == i.uid_id:
            sum_limit = sum_limit + int(i.limit_utilize)
    sum_limit = sum_limit * 5 / 100
    for i in loan:
        if v.id == i.uid_id:
            sum_limit = sum_limit + int(i.emi)
    tot = int(cut - sum_limit)
    ppmm = prod_policy_master.objects.all()
    emi = 0
    elig = 0
    for mn in loan:
        if mn.uid_id == v.id:
            for i in l:
                for k in ppmm:
                    if i == k.pp_id:
                        p = 100000
                        roi = int(k.roi) / (12 * 100)
                        t = v.tenure
                        emi = (p * roi * pow(1 + roi, t)) / (pow(1 + roi, t) - 1)
                        emi = int(emi)
                        elig = int(round(tot / emi, 5) * 100000)
                        if elig > v.loan_amt:
                            foi = v.loan_amt
                        else:
                            foi = elig
                        eligible = elig * co
                        eligible = round(eligible, 2)
            if eligible > camt:
                alamt1 = camt
            else:
                alamt1 = eligible
    for i in loan:
        if i.uid_id == v.id:
            if int(alamt) > elig:
                final = elig
                if final > v.loan_amt:
                    final = v.loan_amt
            else:
                final = int(alamt)
                if final > v.loan_amt:
                    final = v.loan_amt
    return render(request, 'check_el.html',
                  {'foi': foi, 'mul': mul, 'cate': cate, 'final': final, 'alamt1': alamt1, 'camt': camt,
                   'eligible': eligible, 'elig': elig, 'emi': emi, 'tot': tot, 'ob': sum_limit, 'cut': cut, 's': v,
                   'loan': loan, 'credit': credit, 'cat': cat, 'elamt': elamt, 'alamt': alamt, 'cv': cv, 'prod': prod,
                   'msg': msg, 'co': co})


# def sendSimpleEmail(request,id):
#    v = uploads.objects.get(id=id)
#    emailto = v.email
#    res = send_mail("Eligibility check by Creative Finserve", "Your documents have been verified", "siddhi3107.com", [emailto],fail_silently=False)
#
#    return redirect(customer)

# Customer Details End


#                                                -------------------------------------------
# Derived Residence Start
def derived_residence(request):
    a = residence_type.objects.all()
    return render(request, 'derived_residence.html', {'alldata': a})


def add_derived_residence(request):
    return render(request, 'add_derived_res.html')


def add_derived_residence_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = residence_type(r_type=type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(derived_residence)


def res_delete(request, id):
    m = residence_type.objects.get(pk=id).delete()
    return redirect('/crm_app/derived_residence')


# Derived Residence End

#                                                -------------------------------------------
# Derived Salary Start
def derived_salary(request):
    a = salary_type.objects.all()
    return render(request, 'derived_salary.html', {'alldata': a})


def add_derived_salary(request):
    return render(request, 'add_derived_sal.html')


def add_derived_salary_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = salary_type(s_type=type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(derived_salary)


def sal_delete(request, id):
    m = salary_type.objects.get(pk=id).delete()
    return redirect('/crm_app/derived_salary')


# Derived Salary End


#                                                -------------------------------------------
# Derived Company Start
def derived_company(request):
    a = company_type.objects.all()
    return render(request, 'derived_company.html', {'alldata': a})


def add_derived_company(request):
    return render(request, 'add_derived_com.html')


def add_derived_company_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = company_type(co_type=type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(derived_company)


def com_delete(request, id):
    m = company_type.objects.get(pk=id).delete()
    return redirect('/crm_app/derived_company')


# Derived Company End


#                                                -------------------------------------------
# Derived Cocat Start
def derived_cocat(request):
    a = cocat_type.objects.all()
    return render(request, 'derived_cocat.html', {'alldata': a})


def add_derived_cocat(request):
    return render(request, 'add_derived_coc.html')


def add_derived_cocat_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = cocat_type(c_type=type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(derived_cocat)


def coc_delete(request, id):
    m = cocat_type.objects.get(pk=id).delete()
    return redirect('/crm_app/derived_cocat')


# Derived Cocat End

#                                                -------------------------------------------
# Derived Tenure Start
def derived_ten(request):
    a = tenure.objects.all()
    return render(request, 'derived_ten.html', {'alldata': a})


def add_derived_ten(request):
    return render(request, 'add_derived_ten.html')


def add_derived_ten_table(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        o = tenure(tenure=type)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(derived_ten)


def ten_delete(request, id):
    m = tenure.objects.get(pk=id).delete()
    return redirect('/crm_app/derived_ten')


# Derived Tenure End


#                                       -------------------------------
# Reasons Start
def reasonsp(request):
    a = reasons.objects.all()
    return render(request, 'reasons.html', {'alldata': a})


def add_rea(request):
    a = reasons.objects.all()
    return render(request, 'add_rea.html', {'prd': a})


def add_rea_table(request):
    if request.method == 'POST':
        rname = request.POST.get('rname')
        rrea = request.POST.get('rrea')
        o = reasons(rname=rname, rrea=rrea)
        o.save()
        # pyautogui.alert("Upload Done")
    return redirect(reasonsp)


def rea_edit(request, id):
    m = reasons.objects.get(id=id)
    return render(request, 'rea_edit.html', {'prd': m})


def rea_edit_table(request):
    try:
        if request.method == 'POST':
            rname = request.POST.get('rname')
            rrea = request.POST.get('rrea')
            pid = request.POST.get('id')
            abc = reasons.objects.get(id=pid)
            abc.rname = rname
            abc.rrea = rrea
            abc.save()
        return redirect(reasonsp)
    except:
        return render(request, 'failure.html')


def rea_delete(request, id):
    m = reasons.objects.get(pk=id).delete()
    return redirect('/crm_app/reasonsp')


# Reasons End

#                                                -------------------------------------------
# Foir Start
def master_foir(request):
    a = pp_foir.objects.all()
    return render(request, 'master_foir.html', {'alldata': a})


def add_foir(request):
    a = prod_policy_master.objects.all()
    return render(request, 'add_foir.html', {'a': a})


def add_foir_table(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        sid = prod_policy_master.objects.get(id=pid)
        min_amt = request.POST.get('min_amt')
        max_amt = request.POST.get('max_amt')
        cutoff = request.POST.get('cutoff')
        if pp_foir.objects.filter(ppid7=pid, min_amt=min_amt, max_amt=max_amt):
            return render(request, 'foir_error.html')
        else:
            o = pp_foir(ppid7=sid, min_amt=min_amt, max_amt=max_amt, cutoff=cutoff)
            o.save()
        # pyautogui.alert("Upload Done")
    return redirect('/crm_app/master_product_policy')


def foir_edit_table(request):
    try:
        if request.method == 'POST':
            min_amt = request.POST.get('min_amt')
            max_amt = request.POST.get('max_amt')
            cutoff = request.POST.get('cutoff')
            pid = request.POST.get('id')

            abc = pp_foir.objects.get(id=pid)
            abc.min_amt = min_amt
            abc.max_amt = max_amt
            abc.cutoff = cutoff
            abc.save()
        return redirect('/crm_app/master_product_policy')
    except:
        return render(request, 'failure.html')


def foir_edit(request, id):
    m = pp_foir.objects.get(pk=id)
    return render(request, 'foir_edit.html', {'prd': m})


def foir_delete(request, id):
    m = pp_foir.objects.get(pk=id).delete()
    return redirect('/crm_app/master_product_policy')


# Foir End

def cust_delete(request, id):
    m = uploads.objects.get(pk=id).delete()
    return redirect('/crm_app/customer')


def add_customer_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        e_mail = request.POST.get('email')
        loan_type = request.POST.get('loan_type')
        custo_type = request.POST.get('custo_type')
        if request.POST.get('ten') != "Select":
            ten = request.POST.get('ten')
        else:
            ten = 0
        mobile_no = request.POST.get('mobile')
        if request.POST.get('cibil_score'):
            cibil_score = request.POST.get('cibil_score')
        else:
            cibil_score = "0"
        bank_name = request.POST.get('bank_name')
        if request.POST.get('gross_sal'):
            gross_sal = request.POST.get('gross_sal')
        else:
            gross_sal = "0"
        if request.POST.get('net_sal'):
            net_sal = request.POST.get('net_sal')
        else:
            net_sal = "0"
        if request.POST.get('age'):
            age = request.POST.get('age')
        else:
            age = "0"
        if request.POST.get('retire_age'):
            retire_age = request.POST.get('retire_age')
        else:
            retire_age = "0"
        company_type = request.POST.get('company_type')
        company_name = request.POST.get('company_name')
        paid_up_cap = ''
        company_yrs = ''
        nature_company = ''
        designation = request.POST.get('designation')
        designation_type = request.POST.get('designation_type')
        if request.POST.get('current_exp'):
            current_exp = request.POST.get('current_exp')
        else:
            current_exp = "0"
        if request.POST.get('total_exp'):
            total_exp = request.POST.get('total_exp')
        else:
            total_exp = "0"
        emp_type = request.POST.get('emp_type')
        form_16 = request.POST.get('form_16')
        residence_type = request.POST.get('residence_type')
        stt = request.POST.get('stt')
        sttt = request.POST.get('sttt')
        if request.POST.get('loan_amt'):
            loan_amt = request.POST.get('loan_amt')
        else:
            loan_amt = 0
        try:
            obj = uploads.objects.latest('id')
            uid = obj.id + 1
        except uploads.DoesNotExist:
            uid = 1
        o = uploads(id=uid, name=name, mobile=mobile_no, email=e_mail, loan_type=loan_type, custo_type=custo_type,
                    tenure=ten, cibil_score=cibil_score, bank_name=bank_name, gross_sal=gross_sal, net_sal=net_sal,
                    age=age, retire_age=retire_age, company_type=company_type, company_name=company_name,
                    paid_up_cap=paid_up_cap, company_yrs=company_yrs, nature_company=nature_company,
                    designation=designation,
                    designation_type=designation_type, current_exp=current_exp, total_exp=total_exp, emp_type=emp_type,
                    form_16=form_16, residence_type=residence_type, stt=stt, sttt=sttt, criteria='', remark='',
                    loan_amt=loan_amt, date=str(datetime.now())[:22]
                    )
        o.save()
        l_bank = request.POST.getlist('l_bank')
        l_product = request.POST.getlist('l_product')
        l_loan = request.POST.getlist('l_loan')
        l_emi = request.POST.getlist('l_emi')
        l_roi = request.POST.getlist('l_roi')
        l_emi_start = request.POST.getlist('l_emi_start')
        l_emi_end = request.POST.getlist('l_emi_end')
        l_bounces = request.POST.getlist('l_bounces')
        l_moratorium = request.POST.getlist('l_moratorium')

        c_bank = request.POST.getlist('c_bank')
        c_credit_limit = request.POST.getlist('c_credit_limit')
        c_limit_utilize = request.POST.getlist('c_limit_utilize')
        c_card_age = request.POST.getlist('c_card_age')
        c_payment_delay = request.POST.getlist('c_payment_delay')
        c_moratorium = request.POST.getlist('c_moratorium')

        if l_emi != ['']:
            for (a, b, c, d, e, f, g, h, i) in zip(l_bank, l_product, l_loan, l_emi, l_roi, l_emi_start, l_emi_end,
                                                   l_bounces, l_moratorium):
                abc = loan_details(uid_id=uid, bank=a, product=b, loan=c, emi=d, roi=e, emi_start=f, emi_end=g,
                                   bounces=h, moratorium=i)
                abc.save()

        if c_limit_utilize != ['']:
            for (a, b, c, d, e, f) in zip(c_bank, c_credit_limit, c_limit_utilize, c_card_age, c_payment_delay,
                                          c_moratorium):
                abc = credit_details(uid_id=uid, bank=a, credit_limit=b, limit_utilize=c, card_age=d, payment_delay=e,
                                     moratorium=f)
                abc.save()

    return redirect('/crm_app/checks/' + str(uid))


def add_customer(request):
    custo_type = customer_type.objects.all().distinct()
    co = companyName.objects.all()
    l = loan_type.objects.all()
    t = tenure.objects.all()
    b = company_type.objects.all()
    c = designation.objects.all()
    d = residence_type.objects.all()
    e = bank_cat.objects.all()
    return render(request, 'add_customer.html',
                  {'co': co, 'custo_type': custo_type, 't': t, 'loan_type': l, 'com_type': b, 'des': c, 'res': d,
                   'com_name': e})


# CALCULATION
t21 = 0
t3 = 0
t1 = 0
l1 = []
l4 = []
l5 = []
l6 = []
e = 0
no = 1
namount = 0
typ = 0
gst, Bcharges, Install_no, fc, amt, intr, emi, years, months, days, totalamt, totalint, p, c = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


def index_calc(request):
    global t1, t21, t3, l1, l4, l5, l6, e, gst, Bcharges, Install_no, fc, amt, intr, l1, l6, l4, l5, emi, years, months, days, totalamt, totalint, p, c, typ
    if request.method == 'POST':
        choice = request.POST.get('type')
        amount = float(request.POST['amount'])
        amt = float(request.POST['amount'])
        intrest = float(request.POST['intrest'])
        intr = float(request.POST['intrest'])
        option = int(request.POST['options'])
        if (option == 1):
            typ = 'Half year'
        if (option == 2):
            typ = 'Quater'
        if (option == 3):
            typ = 'Month'
        if (option == 4):
            typ = 'Forth nightly'
        if (option == 5):
            typ = 'week'
        if (option == 6):
            typ = 'Day'
        print(typ)
        l1.clear()
        l4.clear()
        l5.clear()
        l6.clear()
        try:
            years = int(request.POST['years'])
        except:
            years = 0
        try:
            months = int(request.POST['months'])
        except:
            months = 0
        try:
            days = int(request.POST['days'])
        except:
            days = 0
        try:
            Install_no = int(request.POST['Install_no'])
        except:
            Install_no = 0
        try:
            Bcharges = float(request.POST['Bank charges'])
        except:
            Bcharges = 0
        try:
            gst = float(request.POST['GST'])
        except:
            gst = 0

        dic = {1: 2, 2: 4, 3: 12, 4: 24, 5: 52, 6: 365}
        if (years != 0):
            t1 = years * dic[option]
        if (months != 0):
            if (option == 3):
                t21 = months * 1
            elif (option == 4):  # 1-HALF Y
                t21 = months * 2  # 2-FOURTH             quater
            elif (option == 2):  # 3-QUATER                      month
                t21 = months / 3  # 4-MONTHLY             forth
            elif (option == 5):  # 5-WEEKLY
                t21 = months * 4  # 6-DAILY
            elif (option == 6):
                t21 = months * 30
            elif (option == 1):
                if (months > 5):
                    t21 = months / 6
                else:
                    message = 'you cannot select since months are less than 5'
                    return render(request, 'invinp.html', {'message': message})

        if (days != 0):
            if (years != 0 or months != 0):
                if (days > 29):
                    message = ' YOU CANNOT more than 29 day'
                    return render(request, 'invinp.html', {'message': message})

                elif (option == 6):
                    t3 = days

                elif (option == 5):
                    t3 = days / 7
                elif (option == 4):
                    if (days > 14):
                        t3 = days / 14
                    else:
                        message = 'you cannot enter days less than 15'
                        return render(request, 'invinp.html', {'message': message})

            elif (months != 0 or years != 0):
                if (option == 6):
                    t3 = days

                elif (option == 5):
                    t3 = days / 7
                elif (option == 4):
                    t3 = days / 14
            else:
                if (option == 6):
                    t3 = days


                elif (option == 5):
                    t3 = days / 7

                elif (option == 4):
                    if (days > 14):
                        t3 = days / 14

                    else:
                        message = 'you cannot enter days less than 15'
                        return render(request, 'invinp.html', {'message': message})

                elif (option == 1 or 2 or 3):
                    message = 'you can select only weeks or days'
                    return render(request, 'invinp.html', {'message': message})
        try:

            t = t1 + t21 + t3
            r = intrest / (100 * dic[option])
            if (int(choice) == 1):
                e = (amount / t) + (amount * r)
            else:
                e = (amount * r * pow((1 + r), t)) / (pow((1 + r), t) - 1)

            totalint = round((e * t) - amount)
            totalamt = round((e * t))

            for i in range(int(t)):
                intrest = r * amount
                pri_pay = e - intrest
                remain = amount - pri_pay
                l1.append(i + 1)
                l4.append(round(intrest))
                l5.append(round(pri_pay))
                l6.append(round(remain))
                amount = remain
            try:
                i = l4[Install_no - 1]
                p = l6[Install_no - 1]
                bi = p * (Bcharges / 100)
                g = (gst / 100) * bi
                c = bi + g
                fc = p + bi + g
            except:
                fc = 0
                c = 0

            t21 = 0
            t3 = 0
            t1 = 0
            amount = 0
            intrest = 0

        except:
            t21 = 0
            t3 = 0
            t1 = 0
            amount = 0
            intrest = 0
            typ = 0
            return render(request, 'error.html')

        if (int(choice) == 1):
            return render(request, "flat.html",
                          {'typ': typ, 'amt': amt, 'intr': intr, 'amount': amount, 'intrest': intrest, 'emi': round(e),
                           'years': years, 'months': months, 'days': days, 'totalint': totalint, 'totalamt': totalamt})
        else:
            return render(request, "reducing.html",
                          {'typ': typ, 'p': p, 'c': round(c), 'gst': gst, 'Bcharges': Bcharges,
                           'Install_no': Install_no, 'fc': round(fc), 'amt': amt, 'intr': intr, 'amount': amount,
                           'intrest': intrest, 'l1': l1, 'l6': l6, 'l5': l5, 'l4': l4, 'emi': round(e), 'years': years,
                           'months': months, 'days': days, 'totalint': totalint, 'totalamt': totalamt})

    return render(request, "index.html")


def advance(request):
    global typ, t1, t21, t3, l1, l4, l5, l6, e, gst, Bcharges, Install_no, fc, amt, intr, l1, l6, l4, l5, emi, years, months, days, totalamt, totalint, no, namount, p, c
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        amt = float(request.POST['amount'])
        intrest = float(request.POST['intrest'])
        intr = float(request.POST['intrest'])
        option = int(request.POST['options'])
        if (option == 1):
            typ = 'Half year'
        if (option == 2):
            typ = 'Quater'
        if (option == 3):
            typ = 'Month'
        if (option == 4):
            typ = 'Forth nightly'
        if (option == 5):
            typ = 'week'
        if (option == 6):
            typ = 'Day'
        print(typ)
        l1.clear()
        l4.clear()
        l5.clear()
        l6.clear()
        try:
            years = int(request.POST['years'])
        except:
            years = 0
        try:
            months = int(request.POST['months'])
        except:
            months = 0
        try:
            days = int(request.POST['days'])
        except:
            days = 0
        try:
            Install_no = int(request.POST['Install_no'])
        except:
            Install_no = 0
        try:
            Bcharges = float(request.POST['Bank charges'])
        except:
            Bcharges = 0
        try:
            no = int(request.POST['no'])
        except:
            no = 1
        try:
            gst = float(request.POST['GST'])
        except:
            gst = 0

        dic = {1: 2, 2: 4, 3: 12, 4: 24, 5: 52, 6: 365}
        if (years != 0):
            t1 = years * dic[option]
        if (months != 0):
            if (option == 3):
                t21 = months * 1
            elif (option == 4):  # 1-HALF Y
                t21 = months * 2  # 2-FOURTH             quater
            elif (option == 2):  # 3-QUATER                      month
                t21 = months / 3  # 4-MONTHLY             forth
            elif (option == 5):  # 5-WEEKLY
                t21 = months * 4  # 6-DAILY
            elif (option == 6):
                t21 = months * 30
            elif (option == 1):
                if (months > 5):
                    t21 = months / 6
                else:
                    message = 'you cannot select since months are less than 5'
                    return render(request, 'invinp.html', {'message': message})

        if (days != 0):
            if (years != 0 or months != 0):
                if (days > 29):
                    message = ' YOU CANNOT more than 29 day'
                    return render(request, 'invinp.html', {'message': message})

                elif (option == 6):
                    t3 = days

                elif (option == 5):
                    t3 = days / 7
                elif (option == 4):
                    if (days > 14):
                        t3 = days / 14
                    else:
                        message = 'you cannot enter days less than 15'
                        return render(request, 'invinp.html', {'message': message})

            elif (months != 0 or years != 0):
                if (option == 6):
                    t3 = days

                elif (option == 5):
                    t3 = days / 7
                elif (option == 4):
                    t3 = days / 14
            else:
                if (option == 6):
                    t3 = days


                elif (option == 5):
                    t3 = days / 7

                elif (option == 4):
                    if (days > 14):
                        t3 = days / 14

                    else:
                        message = 'you cannot enter days less than 15'
                        return render(request, 'invinp.html', {'message': message})

                elif (option == 1 or 2 or 3):
                    message = 'you can select only weeks or days'
                    return render(request, 'invinp.html', {'message': message})
        try:

            t = t1 + t21 + t3
            r = intrest / (100 * dic[option])
            try:
                for i in range(int(no)):
                    intrest = r * amount
                    pri_pay = e - intrest
                    remain = amount - pri_pay
                    l1.append(i + 1)
                    l4.append(round(intrest))
                    l5.append(round(pri_pay))
                    l6.append(round(remain))
                    amount = remain
                ti = sum(l4)
                namount = amt - ti
                l1.clear()
                l4.clear()
                l5.clear()
                l6.clear()
            except:
                namount = amt - (r * amt)
            print(namount)
            e = (namount * r * pow((1 + r), t)) / (pow((1 + r), t) - 1)
            # totalint=round((e*t)-amount)
            totalamt = round((e * t))
            print(e, totalint, totalamt)
            for i in range(int(t)):
                intrest = r * namount
                pri_pay = e - intrest
                remain = namount - pri_pay
                l1.append(i + 1)
                l4.append(round(intrest))
                l5.append(round(pri_pay))
                l6.append(round(remain))
                namount = remain
            for j in range(no):
                l4[j] = 0
                l5[j] = round(e)
            try:
                i = l4[Install_no - 1]
                p = l6[Install_no - 1]
                bi = p * (Bcharges / 100)
                g = (gst / 100) * bi
                c = bi + g
                fc = p + bi + g
            except:
                fc = 0
                c = 0
            t21 = 0
            t3 = 0
            t1 = 0
            amount = 0
            intrest = 0

        except:
            t21 = 0
            t3 = 0
            t1 = 0
            amount = 0
            intrest = 0
            typ = 0
            return render(request, 'error.html')

        return render(request, "advance.html",
                      {'typ': typ, 'p': p, 'c': round(c), 'namount': namount, 'no': no, 'gst': gst,
                       'Bcharges': Bcharges, 'Install_no': Install_no, 'fc': round(fc), 'amt': amt, 'intr': intr,
                       'amount': namount, 'intrest': intrest, 'l1': l1, 'l6': l6, 'l5': l5, 'l4': l4, 'emi': round(e),
                       'years': years, 'months': months, 'days': days, 'totalint': sum(l4), 'totalamt': totalamt})

    return render(request, "advance.html")


def details(request):
    global gst, Bcharges, Install_no, fc, amt, intr, l1, l6, l4, l5, emi, years, months, days, totalamt, totalint, p, c
    return render(request, "details.html",
                  {'typ': typ, 'p': p, 'c': round(c), 'gst': gst, 'Bcharges': Bcharges, 'Install_no': Install_no,
                   'fc': round(fc), 'amt': amt, 'intr': intr, 'l1': l1, 'l6': l6, 'l5': l5, 'l4': l4, 'emi': round(e),
                   'years': years, 'months': months, 'days': days, 'totalint': totalint, 'totalamt': totalamt})


def adetails(request):
    global no, gst, Bcharges, Install_no, fc, amt, intr, l1, l6, l4, l5, emi, years, months, days, totalamt, totalint, p, c
    return render(request, "adetails.html",
                  {'typ': typ, 'p': p, 'c': round(c), 'no': no, 'gst': gst, 'Bcharges': Bcharges,
                   'Install_no': Install_no, 'fc': round(fc), 'amt': amt, 'intr': intr, 'l1': l1, 'l6': l6, 'l5': l5,
                   'l4': l4, 'emi': round(e), 'years': years, 'months': months, 'days': days, 'totalint': totalint,
                   'totalamt': totalamt})


def fdetails(request):
    global amt, emi, years, months, days, totalamt, totalint, typ

    return render(request, "fdetails.html",
                  {'typ': typ, 'amt': amt, 'intr': intr, 'emi': round(e), 'years': years, 'months': months,
                   'days': days, 'totalint': totalint, 'totalamt': totalamt})


'''
def checks(request, id):
    v = uploads.objects.get(id=id)
    p = prod_policy_master.objects.all()
    t = pp_tenure.objects.all()
    res = pp_residence_type.objects.all()
    comp = pp_company_type.objects.all()
    cocat = pp_cocat_type.objects.all()
    b = bank_cat.objects.all()
    c = pp_cibil.objects.all()
    lo = loan_details.objects.all()
    cr = credit_details.objects.all()
    ds = {}
    ds2 = {}
    sid={}
    foircal = 0
    foir = pp_foir.objects.all()
    sid2 = {}
    l = ''
    li = []
    #Salary, Designation, Total Exp, Salary Credit left
    m2 = ''
    set = []
    cal = 0
    cal2 = 0
    msg2 = 0
    for i in p:
        sum = 0
        msg = ''
        amt = 1
        if v.loan_type == i.prod_name:
            msg = msg + i.bank_names + '['
            if v.custo_type == i.type_of_cust:
                msg = msg + 'Salaried, '
                sid[i.bank_names] = 'NOT ELIGIBLE'
                sid2[i.bank_names] = 'NOT ELIGIBLE'
                x = 'NOT ELIGIBLE'
                ds[i.bank_names] = {'tenure':"Tenure not applicable",'category':'I','roi':i.roi,'loanamt':v.loan_amt,'loanelig':"Couldn't be calculated",'loancap':"Couldn't be calculated",'pro':'Not Applicable','elig':'NOT ELIGIBLE','reason':''}
                r = ''
                mal = False
                for o in c:
                    if (o.ppid4_id == i.id) and (int(v.cibil_score) >= o.cibil_type):
                        msg = msg + 'Cibil->' + str(v.cibil_score) + ','
                        mal = True
                if mal != True:
                    r = r + 'Cibil Score not as listed,'
                mal = False
                if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                     mal = True
                if mal != True:
                     r = r + 'Age not in range,'
                mal = False
                if int(v.current_exp) >= i.current_exp:
                    mal = True
                if mal != True:
                    r = r + 'Less Experienced,'
                mal = False
                if (int(v.gross_sal) >= i.salary_new):
                    mal = True
                if mal != True:
                    r = r + 'Less Salary,'
                mal = False
                for m in comp:
                    if m.ppid_id == i.id:
                        if v.company_type == m.comp_type:
                            mal = True
                if mal != True:
                    r = r + 'Company Type not as listed,'
                mal = False
                for j in t:
                    if j.ppid5_id == i.id:
                        if v.tenure == j.ten_type:
                             mal = True
                if mal != True:
                    r = r + 'Tenure not applicable,'
                if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                    msg = msg + 'Age,'
                    if int(v.current_exp) >= i.current_exp:
                        msg = msg + 'Exp,'
                        if (int(v.gross_sal) >= i.salary_new):
                            for m in comp:
                                if m.ppid_id == i.id:
                                    if v.company_type == m.comp_type:
                                        msg = msg + 'CompType' + '->' + v.company_type + ','
                                        for j in t:
                                             if j.ppid5_id == i.id:
                                                  if v.tenure == j.ten_type:
                                                       msg = msg + 'Tenure' + '->' + str(j.ten_type) + ','
                                                       ds[i.bank_names]['tenure'] = v.tenure
                                                       for n in b:
                                                            if v.company_name == n.co_name and i.bank_names == n.bank_name:
                                                                ds[i.bank_names]['category'] = n.cat
                                                                msg = msg + v.company_name + '->' + n.cat + '->'
                                                                for q in cocat:
                                                                    if q.ppid6_id == i.id:
                                                                        if q.cocat_types == n.cat:
                                                                            amt = q.cocat_no * int(v.net_sal)
                                                                            ds[i.bank_names]['loanelig'] = amt
                                                                            msg = msg + str(q.cocat_no) + '->' + str(amt) + ','
                                                                            if amt > q.max_loan_amt:
                                                                                amt = q.max_loan_amt
                                                                            if amt > v.loan_amt:
                                                                                amt = v.loan_amt
                                                                            ds[i.bank_names]['pro'] = i.processing_fee
                                                                            ds[i.bank_names]['loancap'] = amt
                                                                            ds[i.bank_names]['roi'] = i.roi
                                                                            ds[i.bank_names]['loanamt'] = v.loan_amt
                                                                            msg = msg + 'Eligible->' + str(amt) + '{MULTIPLIER}'
                                                                            ds[i.bank_names]['elig'] = 'ELIGIBLE'
                                                                            sid[i.bank_names] = 'ELIGIBLE'
                                                                            x = 'ELIGIBLE'
                                                                for fo in foir:
                                                                    if fo.ppid7_id == i.id:
                                                                        if (int(v.net_sal) > fo.min_amt) and (int(v.net_sal) <= fo.max_amt):
                                                                            cut = int(v.net_sal)*fo.cutoff/100
                                                                            for q in cr:
                                                                                if q.uid_id == v.id:
                                                                                    sum = sum + int(q.limit_utilize)
                                                                                    limit = int(q.limit_utilize)
                                                                            if sum != 0:
                                                                                sum = sum * 5 / 100
                                                                                m2 = m2 + 'Sum->' + str(sum) + '~'
                                                                            for q in lo:
                                                                                if q.uid_id == v.id:
                                                                                     aa = str(q.emi_start)
                                                                                     bb = str(q.emi_end)
                                                                                     a1 = int(aa[:4])
                                                                                     a2 = int(aa[5:7])
                                                                                     a3 = int(aa[8:])
                                                                                     a4 = int(bb[:4])
                                                                                     a5 = int(bb[5:7])
                                                                                     a6 = int(bb[8:])
                                                                                     d1 = date(a1,a2,a3)
                                                                                     d2 = date(a4,a5,a6)
                                                                                     res = abs(d2-d1).days
                                                                                     mon = i.months * 30
                                                                                     if res > mon:
                                                                                        sum = sum + int(q.emi)
                                                                                     m2 = m2 + str(q.emi_start) + '~' + str(q.emi_end) + '~' + str(res) + '~' + str(sum)
                                                                            if sum != 0 and ds[i.bank_names]['tenure']!='Tenure not applicable':
                                                                                ob = sum
                                                                                pri = 100000
                                                                                rate = int(i.roi) / (12 * 100)
                                                                                tenu = v.tenure
                                                                                tot = cut - sum
                                                                                emis = (pri * rate * pow(1 + rate, tenu)) / (pow(1 + rate, tenu) - 1)
                                                                                emis = int(emis)
                                                                                elg = int(round(tot/emis, 5) * 100000)
                                                                                if elg > v.loan_amt:
                                                                                    foi = v.loan_amt
                                                                                else:
                                                                                    foi = elg
                                                                                elgb = elg * cut
                                                                                elgb = round(elgb, 2)
                                                                                ds2[i.bank_names]={'tenure':v.tenure,'cocat':n.cat,'roi':i.roi,'totalemi':int(tot),'elgb':elg,'foi':foi,'pro':i.processing_fee,'elg':'ELIGIBLE','net_sal':v.net_sal,'cutoff':cut,'obligation':ob}
                                                                                sid2[i.bank_names]='ELIGIBLE'
                                                                                foircal = 1

                ds[i.bank_names]['reason'] = r
                cal = cal + 1
                set.append(x)

            msg = msg + ']~~  '
        li.append(msg)
    for value in set:
        if value == 'NOT ELIGIBLE':
            cal2 = cal2 + 1
    if cal == cal2:
        msg2 = 1
    r = remarks.objects.all()
    process = profee.objects.all()
    return render(request, 'check.html', {'ds2':ds2,'msg': msg, 's': v, 'select': l, 'li': li, 'ds': ds, 'r':r, 'sid':sid, 'm2':m2, 'sid2':sid2, 'foircal':foircal,'msg2':msg2,'cal':cal,'cal2':cal2,'set':set,'p':process})
'''


def add_remark(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        rem = request.POST.get('rem')
        names = request.POST.get('names')
        now = datetime.now()
        n = str(now)
        abc = remarks(uid_id=id, rname=names, rdate=n[:19], rem=rem)
        abc.save()
    return redirect('/crm_app/checks/' + id)


def rem_delete(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        remid = request.POST.get('remid')
        id = int(remid)
        m = remarks.objects.get(pk=id).delete()
    return redirect('/crm_app/checks/' + custid)


def add_pro(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        rem = request.POST.get('pro')
        names = request.POST.get('names')
        now = request.POST.get('now')
        abc = profee(uid_id=id, cname=names, pro=rem, rdate=now)
        abc.save()
    return redirect('/crm_app/checks/' + id)


def pro_delete(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        remid = request.POST.get('remid')
        id = int(remid)
        m = profee.objects.get(pk=id).delete()
    return redirect('/crm_app/checks/' + custid)


def master_comp_name(request):
    a = companyName.objects.all()
    return render(request, 'master_comp_name.html', {'alldata': a})


def add_comp_name(request):
    return render(request, 'add_comp_name.html')


def add_comp_name_table(request):
    if request.method == 'POST':
        name = request.POST.get('comp_name')
        o = companyName(compName=name)
        o.save()
        # pyautogui.alert("Upload Done")
    a = companyName.objects.all()
    return render(request, 'master_comp_name.html', {'alldata': a})


def comp_name_edit_table(request):
    try:
        if request.method == 'POST':
            cust_type = request.POST.get('cust_type')
            pid = request.POST.get('id')
            abc = companyName.objects.get(id=pid)
            abc.compName = cust_type
            abc.save()

        a = companyName.objects.all()
        return redirect('/crm_app/master_comp_name')
    except:
        return render(request, 'failure.html')


def comp_name_edit(request, id):
    cust = companyName.objects.get(id=id)
    cust_type = companyName.objects.all()
    return render(request, 'comp_name_edit.html', {'prd': cust, 'cust_type': cust_type})


def checks(request, id):
    v = uploads.objects.get(id=id)
    p = prod_policy_master.objects.all()
    print(p)
    t = pp_tenure.objects.all()
    res = pp_residence_type.objects.all()
    comp = pp_company_type.objects.all()
    cocat = pp_cocat_type.objects.all()
    b = bank_cat.objects.all()
    c = pp_cibil.objects.all()
    lo = loan_details.objects.all()
    cr = credit_details.objects.all()
    ds = {}
    req = 0
    ds2 = {}
    sid = {}
    foircal = 0
    foir = pp_foir.objects.all()
    sid2 = {}
    l = ''
    li = []
    # Salary, Designation, Total Exp, Salary Credit left
    m2 = ''
    set = []
    mulcal = []
    foical = []
    cal = 0
    cal2 = 0
    msg = ''
    msg2 = 0
    for i in p:
        print(i)
        d1 = datetime(int(i.eff_date[:4]), int(i.eff_date[5:7]), int(i.eff_date[8:10]), int(i.eff_date[11:13]),
                      int(i.eff_date[14:16]), int(i.eff_date[17:19]))
        d2 = datetime(int(v.date[:4]), int(v.date[5:7]), int(v.date[8:10]), int(v.date[11:13]), int(v.date[14:16]),
                      int(v.date[17:19]))
        if i.ineff_date != '':
            d3 = datetime(int(i.ineff_date[:4]), int(i.ineff_date[5:7]), int(i.ineff_date[8:10]),
                          int(i.ineff_date[11:13]), int(i.ineff_date[14:16]), int(i.ineff_date[17:19]))
        if (d1 - d2).total_seconds() > 0.0:
            continue
        if i.ineff_date != '':
            if (d2 - d3).total_seconds() > 0.0:
                continue
        sum = 0
        msg = ''
        amt = 1
        roi = 1
        qr = 0
        if v.loan_type == i.prod_name:
            msg = msg + i.bank_names + '['
            if v.custo_type == i.type_of_cust:
                msg = msg + 'Salaried, '
                sid[i.bank_names] = 'NOT ELIGIBLE'
                sid2[i.bank_names] = 'NOT ELIGIBLE'
                x = 'NOT ELIGIBLE'
                ds[i.bank_names] = {'tenure': v.tenure, 'category': "Couldn't be calculated",
                                    'roi': "Couldn't be found",
                                    'loanamt': v.loan_amt, 'loanelig': "Couldn't be calculated",
                                    'loancap': "Couldn't be calculated", 'elig': 'NOT ELIGIBLE',
                                    'pro': i.processing_fee, 'reason': '', 'cocat_no': "Couldn't be calculated"}
                r = ''
                mal = False
                for o in c:
                    if (o.ppid4_id == i.id) and (int(v.cibil_score) >= o.cibil_type):
                        msg = msg + 'Cibil->' + str(v.cibil_score) + ','
                        mal = True
                    if int(v.cibil_score) == 9999 or int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                        mal = False
                if int(v.cibil_score) == 9999:
                    r = r + "CIBIL(9999),"
                    mal = True
                if int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                    r = r + "CIBIL(0 or -1),"
                    mal = True
                if mal != True:
                    for o in c:
                        if o.ppid4_id == i.id:
                            req = o.cibil_type
                    r = r + "Less Cibil(" + str(v.cibil_score) + ")->Required(" + str(req) + "),"
                mal = False
                if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                    mal = True
                if mal != True:
                    r = r + 'Age not in range,'
                mal = False
                if int(v.current_exp) >= i.current_exp:
                    mal = True
                if mal != True:
                    r = r + 'Less Experienced,'
                mal = False
                if int(v.gross_sal) >= i.salary_new:
                    mal = True
                if mal != True:
                    r = r + 'Less Gross Salary,'
                mal = False
                for m in comp:
                    if m.ppid_id == i.id:
                        if v.company_type == m.comp_type:
                            mal = True
                if mal != True:
                    r = r + 'Company Type not as listed,'
                mal = False
                for j in t:
                    if j.ppid5_id == i.id:
                        if v.tenure == j.ten_type:
                            mal = True
                if mal != True:
                    r = r + 'Tenure not applicable,'
                if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                    msg = msg + 'Age,'
                    if int(v.current_exp) >= i.current_exp:
                        msg = msg + 'Exp,'
                        if (int(v.gross_sal) >= i.salary_new):
                            for m in comp:
                                if m.ppid_id == i.id:
                                    if v.company_type == m.comp_type:
                                        msg = msg + 'CompType' + '->' + v.company_type + ','
                                        for j in t:
                                            if j.ppid5_id == i.id:
                                                if v.tenure == j.ten_type:
                                                    msg = msg + 'Tenure' + '->' + str(j.ten_type) + ','
                                                    ds[i.bank_names]['tenure'] = v.tenure
                                                    for n in b:
                                                        if v.company_name == n.co_name and i.bank_names == n.bank_name and n.ineff == '':
                                                            categ = n.cat
                                                            ds[i.bank_names]['category'] = n.cat
                                                            msg = msg + v.company_name + '->' + n.cat + '->'
                                                            for q in cocat:
                                                                if q.ppid6_id == i.id:
                                                                    if q.cocat_types == n.cat:
                                                                        ds[i.bank_names]['cocat_no'] = q.cocat_no
                                                                        roi = q.roi
                                                                        amt = q.cocat_no * int(v.net_sal)
                                                                        ds[i.bank_names]['loanelig'] = amt
                                                                        msg = msg + str(q.cocat_no) + '->' + str(
                                                                            amt) + ','
                                                                        if amt > q.max_loan_amt:
                                                                            amt = q.max_loan_amt
                                                                        if amt > v.loan_amt:
                                                                            amt = v.loan_amt
                                                                        ds[i.bank_names]['loancap'] = amt
                                                                        mulcal.append(amt)
                                                                        ds[i.bank_names]['roi'] = roi
                                                                        ds[i.bank_names]['loanamt'] = v.loan_amt

                                                                        msg = msg + 'Eligible->' + str(
                                                                            amt) + '{MULTIPLIER}'
                                                                        ds[i.bank_names]['elig'] = 'ELIGIBLE'
                                                                        sid[i.bank_names] = 'ELIGIBLE'
                                                                        x = 'ELIGIBLE'
                                                            for fo in foir:
                                                                if fo.ppid7_id == i.id:
                                                                    if (int(v.net_sal) > fo.min_amt) and (
                                                                            int(v.net_sal) <= fo.max_amt):
                                                                        cut = int(v.net_sal) * fo.cutoff / 100
                                                                        for q in cr:
                                                                            if q.uid_id == v.id:
                                                                                sum = sum + int(q.limit_utilize)
                                                                                limit = int(q.limit_utilize)

                                                                        if sum != 0:
                                                                            sum = sum * 5 / 100
                                                                            m2 = m2 + 'Sum->' + str(sum) + '~'
                                                                        creditob = sum
                                                                        ab = 0
                                                                        for q in lo:
                                                                            if q.uid_id == v.id:
                                                                                loanob = 'Enter'
                                                                                aa = str(q.emi_start)
                                                                                bb = str(q.emi_end)
                                                                                loanob = loanob + '->' + aa + '->' + bb
                                                                                a1 = int(aa[:4])
                                                                                a2 = int(aa[5:7])
                                                                                a3 = int(aa[8:])
                                                                                a4 = int(bb[:4])
                                                                                a5 = int(bb[5:7])
                                                                                a6 = int(bb[8:])
                                                                                d1 = date(a1, a2, a3)
                                                                                d2 = date(a4, a5, a6)
                                                                                res = abs(d2 - d1).days
                                                                                loanob = loanob + '->' + str(res)
                                                                                mon = i.months * 30
                                                                                if res > mon:
                                                                                    sum = sum + int(q.emi)
                                                                                    ab = ab + int(q.emi)
                                                                                    qr = 1
                                                                                m2 = m2 + str(q.emi_start) + '~' + str(
                                                                                    q.emi_end) + '~' + str(
                                                                                    res) + '~' + str(sum)

                                                                        if sum != 0 and ds[i.bank_names][
                                                                            'tenure'] != 'Tenure not applicable' and qr == 1:
                                                                            ob = sum
                                                                            pri = 100000
                                                                            rate = int(roi) / (12 * 100)
                                                                            tenu = v.tenure
                                                                            tot = cut - sum
                                                                            if tot > 0:
                                                                                emis = (pri * rate * pow(1 + rate,
                                                                                                         tenu)) / (
                                                                                               pow(1 + rate,
                                                                                                   tenu) - 1)
                                                                                emis = int(emis)
                                                                                elg = int(round(tot / emis, 5) * 100000)
                                                                                if elg > v.loan_amt:
                                                                                    foi = v.loan_amt
                                                                                else:
                                                                                    foi = elg
                                                                                elgb = elg * cut
                                                                                elgb = round(elgb, 2)

                                                                                ds2[i.bank_names] = {'tenure': v.tenure,
                                                                                                     'cocat': categ,
                                                                                                     'roi': roi,
                                                                                                     'elgb': elg,
                                                                                                     'foi': foi,
                                                                                                     'elg': 'ELIGIBLE',
                                                                                                     'net_sal': v.net_sal,
                                                                                                     'cutoff': int(cut),
                                                                                                     'obligation': int(
                                                                                                         ob),
                                                                                                     'totalemi': int(
                                                                                                         tot),
                                                                                                     'emi': emis,
                                                                                                     'pro': i.processing_fee}
                                                                                foical.append(foi)
                                                                                sid2[i.bank_names] = 'ELIGIBLE'
                                                                                foircal = 1

                ds[i.bank_names]['reason'] = r
                cal = cal + 1
                set.append(x)

            msg = msg + ']~~  '
        li.append(msg)
    for value in set:
        if value == 'NOT ELIGIBLE':
            cal2 = cal2 + 1
    if cal == cal2:
        msg2 = 1
    dict = {}
    mulop = 0
    foiop = 0
    if mulcal != []:
        mulop = 1
        minmul = min(mulcal)
        for i in range(len(mulcal)):
            if mulcal[i] == minmul:
                count = 0
                for j in ds:
                    if i == count:
                        dict[j] = ds[j]
                    count += 1
    dict2 = {}
    if foical != []:
        foiop = 1
        minfoi = min(foical)
        for i in range(len(foical)):
            if foical[i] == minfoi:
                count = 0
                for j in ds2:
                    if i == count:
                        dict2[j] = ds2[j]
                    count += 1
    # Final Eligibility
    fin = {}
    mul, foirs = 0, 0
    for i, j in ds.items():
        fin[i + 'MULTI'] = {'BANK': i, 'LOANAMT': v.loan_amt, 'LOANELIG': ds[i]['loanelig'],
                            'BANKCAP': ds[i]['loancap'], 'PROCESSING': ds[i]['pro'], 'TENURE': ds[i]['tenure'],
                            'ROI': ds[i]['roi'], 'CALCULATE': 'MULTIPLIER', 'ELIG': ds[i]['elig']}
        if ds[i]['loancap'] != "Couldn't be calculated":
            mul += 1
    fin2 = {}
    for m, n in ds2.items():
        fin2[m + 'FOIR'] = {'BANK': m, 'LOANAMT': v.loan_amt, 'LOANELIG': ds2[m]['elgb'], 'BANKCAP': ds2[m]['foi'],
                            'PROCESSING': ds2[m]['pro'], 'TENURE': ds[i]['tenure'], 'ROI': ds2[m]['roi'],
                            'CALCULATE': 'FOIR', 'ELIG': 'ELIGIBLE'}

    ## Trials of Final Eligibility
    exist = 0
    finalize, finalize2 = {}, {}
    if len(fin2) == 0 and mul == 0:
        exist = 0
    elif len(fin2) == 0 and mul != 0:
        for i, j in fin.items():
            finalize[i] = fin[i]
    elif len(fin2) != 0 and mul != 0:
        for i, j in fin.items():
            if fin[i]['BANKCAP'] != "Couldn't be calculated":
                mno = 0
                for m, n in fin2.items():
                    if fin[i]['BANK'] == fin2[m]['BANK']:
                        if fin[i]['BANKCAP'] < fin2[m]['BANKCAP']:
                            finalize2[i] = fin[i]
                            mno = 1
                        elif fin[i]['BANKCAP'] >= fin2[m]['BANKCAP']:
                            finalize2[i] = fin2[m]
                            mno = 1
                if mno == 0:
                    finalize2[i] = fin[i]

    if len(finalize) != 0 or len(finalize2) != 0:
        exist = 1

    # Rejection Reasons
    reject = {}
    if mul == 0:
        for i, j in ds.items():
            if ds[i]['elig'] == 'NOT ELIGIBLE':
                reject[i] = {'BANK': i, 'LOANAMT': v.loan_amt, 'LOANELIG': ds[i]['loanelig'],
                             'BANKCAP': ds[i]['loancap'], 'PROCESSING': ds[i]['pro'], 'TENURE': ds[i]['tenure'],
                             'ROI': ds[i]['roi'],
                             'CALCULATE': 'MULTIPLIER', 'ELIGIBILITY': ds[i]['elig'], 'REASON': ds[i]['reason']}

    r = remarks.objects.all()
    process = profee.objects.all()

    return render(request, 'check.html',
                  {'ds2': ds2, 'msg': msg, 's': v, 'select': l, 'li': li, 'ds': ds, 'r': r, 'sid': sid, 'm2': m2,
                   'sid2': sid2, 'foircal': foircal, 'msg2': msg2, 'cal': cal, 'cal2': cal2, 'set': set, 'p': process,
                   'mulcal': mulcal, 'foical': foical, 'dict': dict, 'dict2': dict2, 'mulop': mulop, 'foiop': foiop,
                   'finalize': finalize, 'exist': exist, 'reject': reject, 'mul': mul, 'finalize2': finalize2,
                   'fin': fin})


def loan_edit(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        m = uploads.objects.get(id=custid)
        id = request.POST.get('id')
        n = loan_details.objects.get(id=id)
    return render(request, 'loan_edit.html', {'m': m, 'n': n})


def loan_edit_table(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        id = request.POST.get('id')
        bank = request.POST.get('bank')
        product = request.POST.get('product')
        loan = request.POST.get('loan')
        emi = request.POST.get('emi')
        roi = request.POST.get('roi')
        emi_start = request.POST.get('emi_start')
        emi_end = request.POST.get('emi_end')
        bounces = request.POST.get('bounces')
        moratorium = request.POST.get('moratorium')
        abc = loan_details.objects.get(id=id)
        abc.bank = bank
        abc.product = product
        abc.loan = loan
        abc.emi = emi
        abc.roi = roi
        abc.bounces = bounces
        abc.moratorium = moratorium
        abc.save()
    return redirect('/crm_app/cust_edit/' + str(custid))


def credit_edit(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        m = uploads.objects.get(id=custid)
        id = request.POST.get('id')
        n = credit_details.objects.get(id=id)
    return render(request, 'credit_edit.html', {'m': m, 'n': n})


def credit_edit_table(request):
    if request.method == 'POST':
        custid = request.POST.get('custid')
        id = request.POST.get('id')
        bank = request.POST.get('bank')
        credit_limit = request.POST.get('credit_limit')
        limit_utilize = request.POST.get('limit_utilize')
        card_age = request.POST.get('card_age')
        payment_delay = request.POST.get('payment_delay')
        moratorium = request.POST.get('moratorium')
        abc = credit_details.objects.get(id=id)
        abc.bank = bank
        abc.credit_limit = credit_limit
        abc.limit_utilize = limit_utilize
        abc.card_age = card_age
        abc.payment_delay = payment_delay
        abc.moratorium = moratorium
        abc.save()
    return redirect('/crm_app/cust_edit/' + str(custid))


def smail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        id = request.POST.get('id')
        v = uploads.objects.get(id=id)
        p = prod_policy_master.objects.all()
        t = pp_tenure.objects.all()
        res = pp_residence_type.objects.all()
        comp = pp_company_type.objects.all()
        cocat = pp_cocat_type.objects.all()
        b = bank_cat.objects.all()
        c = pp_cibil.objects.all()
        lo = loan_details.objects.all()
        cr = credit_details.objects.all()
        ds = {}
        req = 0
        ds2 = {}
        sid = {}
        foircal = 0
        foir = pp_foir.objects.all()
        sid2 = {}
        l = ''
        li = []
        # Salary, Designation, Total Exp, Salary Credit left
        m2 = ''
        set = []
        mulcal = []
        foical = []
        cal = 0
        cal2 = 0
        msg = ''
        msg2 = 0
        for i in p:
            d1 = datetime(int(i.eff_date[:4]), int(i.eff_date[5:7]), int(i.eff_date[8:10]), int(i.eff_date[11:13]),
                          int(i.eff_date[14:16]), int(i.eff_date[17:19]))
            d2 = datetime(int(v.date[:4]), int(v.date[5:7]), int(v.date[8:10]), int(v.date[11:13]), int(v.date[14:16]),
                          int(v.date[17:19]))
            if i.ineff_date != '':
                d3 = datetime(int(i.ineff_date[:4]), int(i.ineff_date[5:7]), int(i.ineff_date[8:10]),
                              int(i.ineff_date[11:13]), int(i.ineff_date[14:16]), int(i.ineff_date[17:19]))
            if (d1 - d2).total_seconds() > 0.0:
                continue
            if i.ineff_date != '':
                if (d2 - d3).total_seconds() > 0.0:
                    continue
            sum = 0
            msg = ''
            amt = 1
            roi = 1
            qr = 0
            if v.loan_type == i.prod_name:
                msg = msg + i.bank_names + '['
                if v.custo_type == i.type_of_cust:
                    msg = msg + 'Salaried, '
                    sid[i.bank_names] = 'NOT ELIGIBLE'
                    sid2[i.bank_names] = 'NOT ELIGIBLE'
                    x = 'NOT ELIGIBLE'
                    ds[i.bank_names] = {'tenure': v.tenure, 'category': "Couldn't be calculated",
                                        'roi': "Couldn't be found",
                                        'loanamt': v.loan_amt, 'loanelig': "Couldn't be calculated",
                                        'loancap': "Couldn't be calculated", 'elig': 'NOT ELIGIBLE',
                                        'pro': i.processing_fee, 'reason': '', 'cocat_no': "Couldn't be calculated"}
                    r = ''
                    mal = False
                    for o in c:
                        if (o.ppid4_id == i.id) and (int(v.cibil_score) >= o.cibil_type):
                            msg = msg + 'Cibil->' + str(v.cibil_score) + ','
                            mal = True
                        if int(v.cibil_score) == 9999 or int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                            mal = False
                    if int(v.cibil_score) == 9999:
                        r = r + "CIBIL(9999),"
                        mal = True
                    if int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                        r = r + "CIBIL(0 or -1),"
                        mal = True
                    if mal != True:
                        for o in c:
                            if o.ppid4_id == i.id:
                                req = o.cibil_type
                        r = r + "Less Cibil(" + str(v.cibil_score) + ")->Required(" + str(req) + "),"
                    mal = False
                    if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                        mal = True
                    if mal != True:
                        r = r + 'Age not in range,'
                    mal = False
                    if int(v.current_exp) >= i.current_exp:
                        mal = True
                    if mal != True:
                        r = r + 'Less Experienced,'
                    mal = False
                    if int(v.gross_sal) >= i.salary_new:
                        mal = True
                    if mal != True:
                        r = r + 'Less Gross Salary,'
                    mal = False
                    for m in comp:
                        if m.ppid_id == i.id:
                            if v.company_type == m.comp_type:
                                mal = True
                    if mal != True:
                        r = r + 'Company Type not as listed,'
                    mal = False
                    for j in t:
                        if j.ppid5_id == i.id:
                            if v.tenure == j.ten_type:
                                mal = True
                    if mal != True:
                        r = r + 'Tenure not applicable,'
                    if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                        msg = msg + 'Age,'
                        if int(v.current_exp) >= i.current_exp:
                            msg = msg + 'Exp,'
                            if (int(v.gross_sal) >= i.salary_new):
                                for m in comp:
                                    if m.ppid_id == i.id:
                                        if v.company_type == m.comp_type:
                                            msg = msg + 'CompType' + '->' + v.company_type + ','
                                            for j in t:
                                                if j.ppid5_id == i.id:
                                                    if v.tenure == j.ten_type:
                                                        msg = msg + 'Tenure' + '->' + str(j.ten_type) + ','
                                                        ds[i.bank_names]['tenure'] = v.tenure
                                                        for n in b:
                                                            if v.company_name == n.co_name and i.bank_names == n.bank_name and n.ineff == '':
                                                                categ = n.cat
                                                                ds[i.bank_names]['category'] = n.cat
                                                                msg = msg + v.company_name + '->' + n.cat + '->'
                                                                for q in cocat:
                                                                    if q.ppid6_id == i.id:
                                                                        if q.cocat_types == n.cat:
                                                                            ds[i.bank_names]['cocat_no'] = q.cocat_no
                                                                            roi = q.roi
                                                                            amt = q.cocat_no * int(v.net_sal)
                                                                            ds[i.bank_names]['loanelig'] = amt
                                                                            msg = msg + str(q.cocat_no) + '->' + str(
                                                                                amt) + ','
                                                                            if amt > q.max_loan_amt:
                                                                                amt = q.max_loan_amt
                                                                            if amt > v.loan_amt:
                                                                                amt = v.loan_amt
                                                                            ds[i.bank_names]['loancap'] = amt
                                                                            mulcal.append(amt)
                                                                            ds[i.bank_names]['roi'] = roi
                                                                            ds[i.bank_names]['loanamt'] = v.loan_amt

                                                                            msg = msg + 'Eligible->' + str(
                                                                                amt) + '{MULTIPLIER}'
                                                                            ds[i.bank_names]['elig'] = 'ELIGIBLE'
                                                                            sid[i.bank_names] = 'ELIGIBLE'
                                                                            x = 'ELIGIBLE'
                                                                for fo in foir:
                                                                    if fo.ppid7_id == i.id:
                                                                        if (int(v.net_sal) > fo.min_amt) and (
                                                                                int(v.net_sal) <= fo.max_amt):
                                                                            cut = int(v.net_sal) * fo.cutoff / 100
                                                                            for q in cr:
                                                                                if q.uid_id == v.id:
                                                                                    sum = sum + int(q.limit_utilize)
                                                                                    limit = int(q.limit_utilize)

                                                                            if sum != 0:
                                                                                sum = sum * 5 / 100
                                                                                m2 = m2 + 'Sum->' + str(sum) + '~'
                                                                            creditob = sum
                                                                            ab = 0
                                                                            for q in lo:
                                                                                if q.uid_id == v.id:
                                                                                    loanob = 'Enter'
                                                                                    aa = str(q.emi_start)
                                                                                    bb = str(q.emi_end)
                                                                                    loanob = loanob + '->' + aa + '->' + bb
                                                                                    a1 = int(aa[:4])
                                                                                    a2 = int(aa[5:7])
                                                                                    a3 = int(aa[8:])
                                                                                    a4 = int(bb[:4])
                                                                                    a5 = int(bb[5:7])
                                                                                    a6 = int(bb[8:])
                                                                                    d1 = date(a1, a2, a3)
                                                                                    d2 = date(a4, a5, a6)
                                                                                    res = abs(d2 - d1).days
                                                                                    loanob = loanob + '->' + str(res)
                                                                                    mon = i.months * 30
                                                                                    if res > mon:
                                                                                        sum = sum + int(q.emi)
                                                                                        ab = ab + int(q.emi)
                                                                                        qr = 1
                                                                                    m2 = m2 + str(
                                                                                        q.emi_start) + '~' + str(
                                                                                        q.emi_end) + '~' + str(
                                                                                        res) + '~' + str(sum)

                                                                            if sum != 0 and ds[i.bank_names][
                                                                                'tenure'] != 'Tenure not applicable' and qr == 1:
                                                                                ob = sum
                                                                                pri = 100000
                                                                                rate = int(roi) / (12 * 100)
                                                                                tenu = v.tenure
                                                                                tot = cut - sum
                                                                                if tot > 0:
                                                                                    emis = (pri * rate * pow(1 + rate,
                                                                                                             tenu)) / (
                                                                                                   pow(1 + rate,
                                                                                                       tenu) - 1)
                                                                                    emis = int(emis)
                                                                                    elg = int(
                                                                                        round(tot / emis, 5) * 100000)
                                                                                    if elg > v.loan_amt:
                                                                                        foi = v.loan_amt
                                                                                    else:
                                                                                        foi = elg
                                                                                    elgb = elg * cut
                                                                                    elgb = round(elgb, 2)

                                                                                    ds2[i.bank_names] = {
                                                                                        'tenure': v.tenure,
                                                                                        'cocat': categ,
                                                                                        'roi': roi,
                                                                                        'elgb': elg,
                                                                                        'foi': foi,
                                                                                        'elg': 'ELIGIBLE',
                                                                                        'net_sal': v.net_sal,
                                                                                        'cutoff': int(cut),
                                                                                        'obligation': int(
                                                                                            ob),
                                                                                        'totalemi': int(
                                                                                            tot),
                                                                                        'emi': emis,
                                                                                        'pro': i.processing_fee}
                                                                                    foical.append(foi)
                                                                                    sid2[i.bank_names] = 'ELIGIBLE'
                                                                                    foircal = 1

                    ds[i.bank_names]['reason'] = r
                    cal = cal + 1
                    set.append(x)

                msg = msg + ']~~  '
            li.append(msg)
        for value in set:
            if value == 'NOT ELIGIBLE':
                cal2 = cal2 + 1
        if cal == cal2:
            msg2 = 1
        dict = {}
        mulop = 0
        foiop = 0
        if mulcal != []:
            mulop = 1
            minmul = min(mulcal)
            for i in range(len(mulcal)):
                if mulcal[i] == minmul:
                    count = 0
                    for j in ds:
                        if i == count:
                            dict[j] = ds[j]
                        count += 1
        dict2 = {}
        if foical != []:
            foiop = 1
            minfoi = min(foical)
            for i in range(len(foical)):
                if foical[i] == minfoi:
                    count = 0
                    for j in ds2:
                        if i == count:
                            dict2[j] = ds2[j]
                        count += 1
        # Final Eligibility
        fin = {}
        mul, foirs = 0, 0
        for i, j in ds.items():
            fin[i + 'MULTI'] = {'BANK': i, 'LOANAMT': v.loan_amt, 'LOANELIG': ds[i]['loanelig'],
                                'BANKCAP': ds[i]['loancap'], 'PROCESSING': ds[i]['pro'], 'TENURE': ds[i]['tenure'],
                                'ROI': ds[i]['roi'], 'CALCULATE': 'MULTIPLIER', 'ELIG': ds[i]['elig']}
            if ds[i]['loancap'] != "Couldn't be calculated":
                mul += 1
        fin2 = {}
        for m, n in ds2.items():
            fin2[m + 'FOIR'] = {'BANK': m, 'LOANAMT': v.loan_amt, 'LOANELIG': ds2[m]['elgb'], 'BANKCAP': ds2[m]['foi'],
                                'PROCESSING': ds2[m]['pro'], 'TENURE': ds[i]['tenure'], 'ROI': ds2[m]['roi'],
                                'CALCULATE': 'FOIR', 'ELIG': 'ELIGIBLE'}

        ## Trials of Final Eligibility
        exist = 0
        finalize, finalize2 = {}, {}
        if len(fin2) == 0 and mul == 0:
            exist = 0
        elif len(fin2) == 0 and mul != 0:
            for i, j in fin.items():
                finalize[i] = fin[i]
        elif len(fin2) != 0 and mul != 0:
            for i, j in fin.items():
                if fin[i]['BANKCAP'] != "Couldn't be calculated":
                    mno = 0
                    for m, n in fin2.items():
                        if fin[i]['BANK'] == fin2[m]['BANK']:
                            if fin[i]['BANKCAP'] < fin2[m]['BANKCAP']:
                                finalize2[i] = fin[i]
                                mno = 1
                            elif fin[i]['BANKCAP'] >= fin2[m]['BANKCAP']:
                                finalize2[i] = fin2[m]
                                mno = 1
                    if mno == 0:
                        finalize2[i] = fin[i]

        if len(finalize) != 0 or len(finalize2) != 0:
            exist = 1

        subject = 'Creative Finserve Personal Loan Eligibility'
        content = 'Thanks for joining us..'
        html = 'Dear ' + v.name + ',<br>' + \
               "Congratulations! Based on the information furnished by you, we are pleased to inform you that you are eligible for Personal Loan. Below are the details:-<br>"
        if exist == 1:
            html = html + '<table border="1" cellspacing="0" cellpadding="5">' + \
                   '<tr>' + \
                   '<th style = "color:black"> Bank Name </th>' + \
                   '<th style = "color:black"> Loan Amount </th>' + \
                   '<th style = "color:black"> Loan Eligibility </th>' + \
                   '<th style = "color:black"> Bank Capping </th>' + \
                   '<th style = "color:black"> Processing Fee </th>' + \
                   '<th style = "color:#CD472A"> Tenure </th>' + \
                   '<th style = "color:#CD472A"> ROI </th>' + \
                   '<th style = "color:#CD472A"> Calculation </th>' + \
                   '<th style = "color:#65c3c4"> ELIGIBILITY </th>' + \
                   '</tr>'
            for key, value in finalize.items():
                html = html + '<tr>'
                for key2, value2 in value.items():
                    html = html + '<td style = "color:#000005">' + str(value2) + '</td>'
                html = html + '</tr>'
            for key, value in finalize2.items():
                html = html + '<tr>'
                for key2, value2 in value.items():
                    html = html + '<td style = "color:#000005">' + str(value2) + '</td>'
                html = html + '</tr>'
            html = html + '</table><br>'
            html = html + "Kindly provide your consent and furnish the below documents for processing your Loan application to the Lenders:- <br>" + \
                   "<center>" + \
                   '<table border="1" cellspacing="0" cellpadding="5">' + \
                   '<tr><th>Personal Loan Documents</th></tr>' + \
                   '<tr><td>Photograph</td></tr>' + \
                   '<tr><td>Clear Aadhar Card Copy</td></tr>' + \
                   '<tr><td>Clear Pancard Copy</td></tr>' + \
                   '<tr><td>Latest Residence Proof</td></tr>' + \
                   '<tr><td>Latest 3 months Salary Slip</td></tr>' + \
                   '<tr><td>Clear Company ID Copy</td></tr>' + \
                   '<tr><td>Last 6 Months Bank Statement</td></tr>' + \
                   '<tr><td>Form 16 / Income Tax Returns of Last 3 Yrs</td></tr>' + \
                   '<tr><td>All Loan Sanction Letter If Any</td></tr>' + \
                   '</table>' + \
                   '</center>' + \
                   '<br>' + \
                   'Creative Finserve is a Corporate Channel Partner and Financial Consultancy with Multiple Banks and NBFC’s. This letter shall not in any way constitute a valid contract or a guarantee to any<br>' + \
                   'terms or rates. This shall be valid for 24 hrs from its issuance and is subject to guideline changes for the industry. The related rights to this letter shall not be assigned.' + \
                   '<br><br>' + \
                   'Regards,<br>' + \
                   'Creative Finserve Pvt Ltd<br><br>' + \
                   'Imran Sable<br>' + \
                   "(CEO)"
            msg = EmailMultiAlternatives(f'{subject}', f'{content}', EMAIL_HOST_USER, [f'{email}'])
            msg.attach_alternative(html, "text/html")
            msg.send()
            return render(request, 'mailsent.html')
        else:
            return render(request, 'errorgen.html')


def whatsapp(request):
    return render(request, 'whatsapp.html')


def wMsg(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        id = request.POST.get('id')
        v = uploads.objects.get(id=id)
        p = prod_policy_master.objects.all()
        t = pp_tenure.objects.all()
        res = pp_residence_type.objects.all()
        comp = pp_company_type.objects.all()
        cocat = pp_cocat_type.objects.all()
        b = bank_cat.objects.all()
        c = pp_cibil.objects.all()
        lo = loan_details.objects.all()
        cr = credit_details.objects.all()
        ds = {}
        req = 0
        ds2 = {}
        sid = {}
        foircal = 0
        foir = pp_foir.objects.all()
        sid2 = {}
        l = ''
        li = []
        # Salary, Designation, Total Exp, Salary Credit left
        m2 = ''
        set = []
        mulcal = []
        foical = []
        cal = 0
        cal2 = 0
        msg = ''
        msg2 = 0
        for i in p:
            d1 = datetime(int(i.eff_date[:4]), int(i.eff_date[5:7]), int(i.eff_date[8:10]), int(i.eff_date[11:13]),
                          int(i.eff_date[14:16]), int(i.eff_date[17:19]))
            d2 = datetime(int(v.date[:4]), int(v.date[5:7]), int(v.date[8:10]), int(v.date[11:13]), int(v.date[14:16]),
                          int(v.date[17:19]))
            if i.ineff_date != '':
                d3 = datetime(int(i.ineff_date[:4]), int(i.ineff_date[5:7]), int(i.ineff_date[8:10]),
                              int(i.ineff_date[11:13]), int(i.ineff_date[14:16]), int(i.ineff_date[17:19]))
            if (d1 - d2).total_seconds() > 0.0:
                continue
            if i.ineff_date != '':
                if (d2 - d3).total_seconds() > 0.0:
                    continue
            sum = 0
            msg = ''
            amt = 1
            roi = 1
            qr = 0
            if v.loan_type == i.prod_name:
                msg = msg + i.bank_names + '['
                if v.custo_type == i.type_of_cust:
                    msg = msg + 'Salaried, '
                    sid[i.bank_names] = 'NOT ELIGIBLE'
                    sid2[i.bank_names] = 'NOT ELIGIBLE'
                    x = 'NOT ELIGIBLE'
                    ds[i.bank_names] = {'tenure': v.tenure, 'category': "Couldn't be calculated",
                                        'roi': "Couldn't be found",
                                        'loanamt': v.loan_amt, 'loanelig': "Couldn't be calculated",
                                        'loancap': "Couldn't be calculated", 'elig': 'NOT ELIGIBLE',
                                        'pro': i.processing_fee, 'reason': '', 'cocat_no': "Couldn't be calculated"}
                    r = ''
                    mal = False
                    for o in c:
                        if (o.ppid4_id == i.id) and (int(v.cibil_score) >= o.cibil_type):
                            msg = msg + 'Cibil->' + str(v.cibil_score) + ','
                            mal = True
                        if int(v.cibil_score) == 9999 or int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                            mal = False
                    if int(v.cibil_score) == 9999:
                        r = r + "CIBIL(9999),"
                        mal = True
                    if int(v.cibil_score) == 0 or int(v.cibil_score) == -1:
                        r = r + "CIBIL(0 or -1),"
                        mal = True
                    if mal != True:
                        for o in c:
                            if o.ppid4_id == i.id:
                                req = o.cibil_type
                        r = r + "Less Cibil(" + str(v.cibil_score) + ")->Required(" + str(req) + "),"
                    mal = False
                    if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                        mal = True
                    if mal != True:
                        r = r + 'Age not in range,'
                    mal = False
                    if int(v.current_exp) >= i.current_exp:
                        mal = True
                    if mal != True:
                        r = r + 'Less Experienced,'
                    mal = False
                    if int(v.gross_sal) >= i.salary_new:
                        mal = True
                    if mal != True:
                        r = r + 'Less Gross Salary,'
                    mal = False
                    for m in comp:
                        if m.ppid_id == i.id:
                            if v.company_type == m.comp_type:
                                mal = True
                    if mal != True:
                        r = r + 'Company Type not as listed,'
                    mal = False
                    for j in t:
                        if j.ppid5_id == i.id:
                            if v.tenure == j.ten_type:
                                mal = True
                    if mal != True:
                        r = r + 'Tenure not applicable,'
                    if (int(v.age) >= i.min_age) and (int(v.age) <= i.max_age):
                        msg = msg + 'Age,'
                        if int(v.current_exp) >= i.current_exp:
                            msg = msg + 'Exp,'
                            if (int(v.gross_sal) >= i.salary_new):
                                for m in comp:
                                    if m.ppid_id == i.id:
                                        if v.company_type == m.comp_type:
                                            msg = msg + 'CompType' + '->' + v.company_type + ','
                                            for j in t:
                                                if j.ppid5_id == i.id:
                                                    if v.tenure == j.ten_type:
                                                        msg = msg + 'Tenure' + '->' + str(j.ten_type) + ','
                                                        ds[i.bank_names]['tenure'] = v.tenure
                                                        for n in b:
                                                            if v.company_name == n.co_name and i.bank_names == n.bank_name and n.ineff == '':
                                                                categ = n.cat
                                                                ds[i.bank_names]['category'] = n.cat
                                                                msg = msg + v.company_name + '->' + n.cat + '->'
                                                                for q in cocat:
                                                                    if q.ppid6_id == i.id:
                                                                        if q.cocat_types == n.cat:
                                                                            ds[i.bank_names]['cocat_no'] = q.cocat_no
                                                                            roi = q.roi
                                                                            amt = q.cocat_no * int(v.net_sal)
                                                                            ds[i.bank_names]['loanelig'] = amt
                                                                            msg = msg + str(q.cocat_no) + '->' + str(
                                                                                amt) + ','
                                                                            if amt > q.max_loan_amt:
                                                                                amt = q.max_loan_amt
                                                                            if amt > v.loan_amt:
                                                                                amt = v.loan_amt
                                                                            ds[i.bank_names]['loancap'] = amt
                                                                            mulcal.append(amt)
                                                                            ds[i.bank_names]['roi'] = roi
                                                                            ds[i.bank_names]['loanamt'] = v.loan_amt

                                                                            msg = msg + 'Eligible->' + str(
                                                                                amt) + '{MULTIPLIER}'
                                                                            ds[i.bank_names]['elig'] = 'ELIGIBLE'
                                                                            sid[i.bank_names] = 'ELIGIBLE'
                                                                            x = 'ELIGIBLE'
                                                                for fo in foir:
                                                                    if fo.ppid7_id == i.id:
                                                                        if (int(v.net_sal) > fo.min_amt) and (
                                                                                int(v.net_sal) <= fo.max_amt):
                                                                            cut = int(v.net_sal) * fo.cutoff / 100
                                                                            for q in cr:
                                                                                if q.uid_id == v.id:
                                                                                    sum = sum + int(q.limit_utilize)
                                                                                    limit = int(q.limit_utilize)

                                                                            if sum != 0:
                                                                                sum = sum * 5 / 100
                                                                                m2 = m2 + 'Sum->' + str(sum) + '~'
                                                                            creditob = sum
                                                                            ab = 0
                                                                            for q in lo:
                                                                                if q.uid_id == v.id:
                                                                                    loanob = 'Enter'
                                                                                    aa = str(q.emi_start)
                                                                                    bb = str(q.emi_end)
                                                                                    loanob = loanob + '->' + aa + '->' + bb
                                                                                    a1 = int(aa[:4])
                                                                                    a2 = int(aa[5:7])
                                                                                    a3 = int(aa[8:])
                                                                                    a4 = int(bb[:4])
                                                                                    a5 = int(bb[5:7])
                                                                                    a6 = int(bb[8:])
                                                                                    d1 = date(a1, a2, a3)
                                                                                    d2 = date(a4, a5, a6)
                                                                                    res = abs(d2 - d1).days
                                                                                    loanob = loanob + '->' + str(res)
                                                                                    mon = i.months * 30
                                                                                    if res > mon:
                                                                                        sum = sum + int(q.emi)
                                                                                        ab = ab + int(q.emi)
                                                                                        qr = 1
                                                                                    m2 = m2 + str(
                                                                                        q.emi_start) + '~' + str(
                                                                                        q.emi_end) + '~' + str(
                                                                                        res) + '~' + str(sum)

                                                                            if sum != 0 and ds[i.bank_names][
                                                                                'tenure'] != 'Tenure not applicable' and qr == 1:
                                                                                ob = sum
                                                                                pri = 100000
                                                                                rate = int(roi) / (12 * 100)
                                                                                tenu = v.tenure
                                                                                tot = cut - sum
                                                                                if tot > 0:
                                                                                    emis = (pri * rate * pow(1 + rate,
                                                                                                             tenu)) / (
                                                                                                   pow(1 + rate,
                                                                                                       tenu) - 1)
                                                                                    emis = int(emis)
                                                                                    elg = int(
                                                                                        round(tot / emis, 5) * 100000)
                                                                                    if elg > v.loan_amt:
                                                                                        foi = v.loan_amt
                                                                                    else:
                                                                                        foi = elg
                                                                                    elgb = elg * cut
                                                                                    elgb = round(elgb, 2)

                                                                                    ds2[i.bank_names] = {
                                                                                        'tenure': v.tenure,
                                                                                        'cocat': categ,
                                                                                        'roi': roi,
                                                                                        'elgb': elg,
                                                                                        'foi': foi,
                                                                                        'elg': 'ELIGIBLE',
                                                                                        'net_sal': v.net_sal,
                                                                                        'cutoff': int(cut),
                                                                                        'obligation': int(
                                                                                            ob),
                                                                                        'totalemi': int(
                                                                                            tot),
                                                                                        'emi': emis,
                                                                                        'pro': i.processing_fee}
                                                                                    foical.append(foi)
                                                                                    sid2[i.bank_names] = 'ELIGIBLE'
                                                                                    foircal = 1

                    ds[i.bank_names]['reason'] = r
                    cal = cal + 1
                    set.append(x)

                msg = msg + ']~~  '
            li.append(msg)
        for value in set:
            if value == 'NOT ELIGIBLE':
                cal2 = cal2 + 1
        if cal == cal2:
            msg2 = 1
        dict = {}
        mulop = 0
        foiop = 0
        if mulcal != []:
            mulop = 1
            minmul = min(mulcal)
            for i in range(len(mulcal)):
                if mulcal[i] == minmul:
                    count = 0
                    for j in ds:
                        if i == count:
                            dict[j] = ds[j]
                        count += 1
        dict2 = {}
        if foical != []:
            foiop = 1
            minfoi = min(foical)
            for i in range(len(foical)):
                if foical[i] == minfoi:
                    count = 0
                    for j in ds2:
                        if i == count:
                            dict2[j] = ds2[j]
                        count += 1
        # Final Eligibility
        fin = {}
        mul, foirs = 0, 0
        for i, j in ds.items():
            fin[i + 'MULTI'] = {'BANK': i, 'LOANAMT': v.loan_amt, 'LOANELIG': ds[i]['loanelig'],
                                'BANKCAP': ds[i]['loancap'], 'PROCESSING': ds[i]['pro'], 'TENURE': ds[i]['tenure'],
                                'ROI': ds[i]['roi'], 'CALCULATE': 'MULTIPLIER', 'ELIG': ds[i]['elig']}
            if ds[i]['loancap'] != "Couldn't be calculated":
                mul += 1
        fin2 = {}
        for m, n in ds2.items():
            fin2[m + 'FOIR'] = {'BANK': m, 'LOANAMT': v.loan_amt, 'LOANELIG': ds2[m]['elgb'], 'BANKCAP': ds2[m]['foi'],
                                'PROCESSING': ds2[m]['pro'], 'TENURE': ds[i]['tenure'], 'ROI': ds2[m]['roi'],
                                'CALCULATE': 'FOIR', 'ELIG': 'ELIGIBLE'}

        ## Trials of Final Eligibility
        exist = 0
        finalize, finalize2 = {}, {}
        if len(fin2) == 0 and mul == 0:
            exist = 0
        elif len(fin2) == 0 and mul != 0:
            for i, j in fin.items():
                finalize[i] = fin[i]
        elif len(fin2) != 0 and mul != 0:
            for i, j in fin.items():
                if fin[i]['BANKCAP'] != "Couldn't be calculated":
                    mno = 0
                    for m, n in fin2.items():
                        if fin[i]['BANK'] == fin2[m]['BANK']:
                            if fin[i]['BANKCAP'] < fin2[m]['BANKCAP']:
                                finalize2[i] = fin[i]
                                mno = 1
                            elif fin[i]['BANKCAP'] >= fin2[m]['BANKCAP']:
                                finalize2[i] = fin2[m]
                                mno = 1
                    if mno == 0:
                        finalize2[i] = fin[i]

        if len(finalize) != 0 or len(finalize2) != 0:
            exist = 1
        html = ''
        for key, value in finalize.items():
            for key2, value2 in value.items():
                html = html + str(key2) + '->' + str(value2) + ',\n'
            html = html + '***\n'
        for key, value in finalize2.items():
            for key2, value2 in value.items():
                html = html + str(key2) + '->' + str(value2) + ',\n'
            html = html + '***\n'

        if exist == 1:
            message = 'CREATIVE FINSERVE PVT. LTD.\n' + 'Eligible Banks Details:\n\n' + html
        else:
            message = 'CREATIVE FINSERVE PVT. LTD.\n\n' + 'Eligible Banks: Not Yet'
        now = datetime.now()
        pywhatkit.sendwhatmsg('+91' + mobile, message, now.hour, now.minute + 2)
        return render(request, 'mailsent.html')
    else:
        return render(request, 'error.')


def gmail(request):
    return render(request, 'gmail.html')


def gMsg(request):
    if request.method == 'POST':
        acc = request.POST.get('acc')
        message = request.POST.get('message')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('siddhi3199@gmail.com', 'sidkad1138')
        server.sendmail('siddhi3199@gmail.com', acc, message)
        return redirect('/crm_app/dash')


def csv(request):
    return render(request, 'csv.html')


def done(request):
    if request.method == 'POST':
        resource = ImportsResource()
        dataset = Dataset()
        bank = request.POST.get('bank')
        s = bank_cat.objects.all()
        for i in s:
            if i.bank_name == bank:
                abc = bank_cat.objects.get(id=i.id)
                abc.ineff = str(datetime.now())[:22]
                abc.save()
        file = request.FILES['myfile']
        if not file.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            pyautogui.alert('WRONG FORMAT')
            return redirect('/crm_app/master_bank_cat')
        imported = dataset.load(file.read(), format='xlsx')
        for i in imported:
            value = bank_cat(
                i[0],
                bank,
                i[1],
                i[2],
                str(datetime.now())[:22],
                ''
            )
            value.save()
        pg.alert('DONEEEE')
        return redirect('/crm_app/master_bank_cat')

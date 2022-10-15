# Create your views here.
from django.shortcuts import render, redirect
#import pyautogui
from .models import uploads, loan_details, credit_details
from crm_app.models import designation, pp_tenure, bank_cat, loan_type, customer_type, pp_company_type, pp_residence_type, company_type, tenure, residence_type, companyName
from datetime import datetime, date
import datetime
# Create your views here.


def upload_details(request):
    custo_type = customer_type.objects.all().distinct()
    l = loan_type.objects.all()
    t = tenure.objects.all()
    b = company_type.objects.all()
    c = designation.objects.all()
    d = residence_type.objects.all()
    e = bank_cat.objects.all()
    co = companyName.objects.all()
    return render(request, 'uploadDoc.html', {'co': co, 'custo_type': custo_type, 't': t, 'loan_type': l, 'com_type': b, 'des': c, 'res': d, 'com_name': e})


'''
def load(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        e_mail = request.POST.get('email')
        loan_type = request.POST.get('loan_type')
        custo_type = request.POST.get('custo_type')
        if request.POST.get('ten')!="Select":
            ten = request.POST.get('ten')
        else:
            ten="0"
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
        paid_up_cap = request.POST.get('paid_up_cap')
        company_yrs = request.POST.get('company_yrs')
        nature_company = request.POST.get('nature_company')
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
        loan_amt = request.POST.get('loan_amt')
        try:
            obj = uploads.objects.latest('id')
            uid = obj.id+1
        except uploads.DoesNotExist:
            uid = 1

        o = uploads(id=uid,loan_amt=loan_amt, name=name, mobile=mobile_no, email=e_mail,loan_type=loan_type,custo_type=custo_type,tenure=ten, cibil_score=cibil_score, bank_name=bank_name, gross_sal=gross_sal, net_sal=net_sal, age=age, retire_age=retire_age, company_type=company_type, company_name=company_name, paid_up_cap=paid_up_cap, company_yrs=company_yrs, nature_company=nature_company, designation=designation, designation_type=designation_type, current_exp=current_exp, total_exp=total_exp, emp_type=emp_type, form_16=form_16, residence_type=residence_type, stt=stt, sttt=sttt)
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
        l_loan_belong = request.POST.getlist('l_loan_belong')

        c_bank = request.POST.getlist('c_bank')
        c_credit_limit = request.POST.getlist('c_credit_limit')
        c_limit_utilize = request.POST.getlist('c_limit_utilize')
        c_card_age = request.POST.getlist('c_card_age')
        c_payment_delay = request.POST.getlist('c_payment_delay')
        c_moratorium = request.POST.getlist('c_moratorium')
        c_card_belong = request.POST.getlist('c_card_belong')

        if l_bank==[] and c_bank==[]:
            l_bank = []
            l_product = []
            l_loan = []
            l_emi = []
            l_roi = []
            l_emi_start = []
            l_emi_end = []
            l_bounces = []
            l_moratorium = []
            l_loan_belong = []

            c_bank = []
            c_credit_limit = []
            c_limit_utilize = []
            c_card_age = []
            c_payment_delay = []
            c_moratorium = []
            c_card_belong = []

        for (a,b,c,d,e,f,g,h,i,j) in zip(l_bank, l_product, l_loan, l_emi, l_roi, l_emi_start, l_emi_end, l_bounces, l_moratorium, l_loan_belong):
            abc = loan_details(uid_id=uid, bank=a, product=b, loan=c, emi=d, roi=e, emi_start=f, emi_end=g, bounces=h, moratorium=i, loan_belong=j)
            abc.save()

        for (a,b,c,d,e,f,g) in zip(c_bank, c_credit_limit, c_limit_utilize, c_card_age, c_payment_delay, c_moratorium, c_card_belong):
            abc = credit_details(uid_id=uid, bank=a, credit_limit=b, limit_utilize=c, card_age=d, payment_delay=e, moratorium=f, card_belong=g)
            abc.save()
            

        #pyautogui.alert("Upload Done")
    return redirect('/')
'''


def load(request):
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
            uid = obj.id+1
        except uploads.DoesNotExist:
            uid = 1
        o = uploads(id=uid, name=name, mobile=mobile_no, email=e_mail, loan_type=loan_type, custo_type=custo_type,
                    tenure=ten, cibil_score=cibil_score, bank_name=bank_name, gross_sal=gross_sal, net_sal=net_sal,
                    age=age, retire_age=retire_age, company_type=company_type, company_name=company_name,
                    paid_up_cap=paid_up_cap, company_yrs=company_yrs, nature_company=nature_company, designation=designation,
                    designation_type=designation_type, current_exp=current_exp, total_exp=total_exp, emp_type=emp_type,
                    form_16=form_16, residence_type=residence_type, stt=stt, sttt=sttt, criteria='', remark='',
                    loan_amt=loan_amt, date=str(datetime.datetime.now())[:22]
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
            for (a, b, c, d, e, f, g, h, i) in zip(l_bank, l_product, l_loan, l_emi, l_roi, l_emi_start, l_emi_end, l_bounces, l_moratorium):
                abc = loan_details(uid_id=uid, bank=a, product=b, loan=c, emi=d,
                                   roi=e, emi_start=f, emi_end=g, bounces=h, moratorium=i)
                abc.save()

        if c_limit_utilize != ['']:
            for (a, b, c, d, e, f) in zip(c_bank, c_credit_limit, c_limit_utilize, c_card_age, c_payment_delay, c_moratorium):
                abc = credit_details(uid_id=uid, bank=a, credit_limit=b,
                                     limit_utilize=c, card_age=d, payment_delay=e, moratorium=f)
                abc.save()

    return redirect('/')

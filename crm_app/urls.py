"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from crm_app import views

urlpatterns = [
    path('index_calc', views.index_calc,name='home'),
    path('advance', views.advance,name='adv'),
    path('details', views.details,name='det'),
    path('adetails', views.adetails,name='adet'),
    path('fdetails', views.fdetails,name='fdet'),
    path('not_listed', views.not_listed, name='Not Listed'),
    path('dash', views.dash, name='CRM Dashboard'),
    path('customer', views.customer, name='Customers Entries'),
    path('logout', views.logout, name='Logout'),
    path('master_cust_type', views.master_cust_type,name='Master Customer Type'),
    path('add_cust_type', views.add_cust_type,name='Add Customer Type'),
    path('add_prd_ply', views.add_prd_ply,name='Add Product & Policy'),
    path('add_cust_type_table', views.add_cust_type_table,name='Add Customer Types'),
    path('master_loan_type', views.master_loan_type,name='Master Loan Type'),
    path('add_loan_type', views.add_loan_type, name='Add loan_type'),
    path('add_loan_type_table', views.add_loan_type_table, name='Add loan_types'),
    path('master_bank_name', views.master_bank_name,name='Master Bank Name'),
    path('add_bank_name', views.add_bank_name, name='Add Bank Name'),
    path('add_bank_name_table', views.add_bank_name_table, name='Add Bank Names'),
    path('add_prd_ply_table', views.add_prd_ply_table1, name='Add Product And Policy'),
    path('add_cocat_type', views.add_cocat_type, name='Add co cat type'),
    path('add_cocat_type_table', views.add_cocat_type_table, name='Add co cat types'),
    path('master_bank_cat', views.master_bank_cat,name='Master Bank Category'),
    path('add_bank_cat', views.add_bank_cat, name='Add bank_cat'),
    path('add_bank_cat_table', views.add_bank_cat_table, name='Add bank_cats'),
    path('add_company_type', views.add_company_type, name='Add company type'),
    path('add_company_type_table', views.add_company_type_table, name='Add company types'),
    path('add_salary_type', views.add_salary_type, name='Add salary_type'),
    path('add_salary_type_table', views.add_salary_type_table, name='Add salary_types'),
    path('add_residence_type', views.add_residence_type, name='Add residence_type'),
    path('add_residence_type_table', views.add_residence_type_table, name='Add residence_types'),
    path('master_designation', views.master_designation,name='Master Designation'),
    path('add_designation', views.add_designation,name='Add designation'),
    path('add_designation_table', views.add_designation_table,name='Add designations'),
    path('load_company', views.load_company, name='ajax_load_company'),
    path('load_cocat', views.load_cocat, name='ajax_load_cocat'),
    path('prd_ply_edit/<int:id>', views.prd_ply_edit, name='Product & Policy Edit'),
    path('prd_ply_edit/prd_ply_edit_table', views.prd_ply_edit_table, name='Edit Product And Policy'),
    path('cust_type_edit/<int:id>', views.cust_type_edit, name='customer type Edit'),
    path('cust_type_edit/cust_type_edit_table', views.cust_type_edit_table, name='Edit Customer Type'),
    path('loan_type_edit/<int:id>', views.loan_type_edit, name='loan type Edit'),
    path('loan_type_edit/loan_type_edit_table', views.loan_type_edit_table, name='Edit loan Type'),
    path('designation_type_edit/<int:id>', views.designation_type_edit, name='designation type Edit'),
    path('designation_type_edit/designation_type_edit_table', views.designation_type_edit_table, name='Edit designation Type'),
    path('bank_name_edit/<int:id>', views.bank_name_edit, name='bank name Edit'),
    path('bank_name_edit/bank_name_edit_table', views.bank_name_edit_table, name='Edit bank name'),
    path('bank_cat_edit/<int:id>', views.bank_cat_edit, name='bank cat Edit'),
    path('bank_cat_edit/bank_cat_edit_table', views.bank_cat_edit_table, name='Edit bank cat'),
    path('bank_cat_delete/<int:id>', views.bank_cat_delete, name='bank_cat_delete'),
    path('add_prod_policy_table', views.add_prod_policy_table),
    #------------------------------------------------ CO-CATEGORY TYPE ---------------------------------------------
    path('cocat_type_edit/<int:id>', views.cocat_type_edit, name='cocat type Edit'),
    path('cocat_type_edit/cocat_type_edit_table', views.cocat_type_edit_table, name='Edit cocat Type'),
    path('master_cocat_type', views.master_cocat_type,name='Master Co-Category Type'),
    path('cocat_type_delete/<int:id>', views.cocat_type_delete, name='cocat_type_delete'),
    #------------------------------------------------ COMPANY TYPE ----------------------------------------------
    path('master_company_type', views.master_company_type,name='Master Company Type'),
    path('company_type_edit/<int:id>', views.company_type_edit, name='company type Edit'),
    path('company_type_edit/company_type_edit_table', views.company_type_edit_table, name='Edit company Type'),
    path('company_type_delete/<int:id>', views.company_type_delete, name='company_type_delete'),
    #------------------------------------------------ SALARY TYPE -----------------------------------------------
    path('master_salary_type', views.master_salary_type,name='Master Salary Type'),
    path('salary_type_edit/<int:id>', views.salary_type_edit, name='salary type Edit'),
    path('salary_type_edit/salary_type_edit_table', views.salary_type_edit_table, name='Edit Salary Type'),
    path('salary_type_delete/<int:id>', views.salary_type_delete, name='salary_type_delete'),
    #------------------------------------------------ CIBIL -----------------------------------------------
    path('add_cibil',views.add_cibil,name='add_cibil'),
    path('add_cibil_table',views.add_cibil_table,name='add_cibil_table'),
    path('master_cibil', views.master_cibil,name='Master cibil'),
    path('cibil_edit/<int:id>', views.cibil_edit, name='cibil_edit'),
    path('cibil_edit/cibil_edit_table', views.cibil_edit_table, name='Edit cibil'),
    path('cibil_delete/<int:id>', views.cibil_delete, name='cibil_delete'),
    #------------------------------------------------ TENURE -----------------------------------------------
    path('add_tenure',views.add_tenure,name='add_tenure'),
    path('add_tenure_table',views.add_tenure_table,name='add_tenure_table'),
    path('master_tenure', views.master_tenure,name='Master tenure'),
    path('tenure_edit/<int:id>', views.tenure_edit, name='tenure Edit'),
    path('tenure_edit/tenure_edit_table', views.tenure_edit_table, name='Edit tenure'),
    path('tenure_delete/<int:id>', views.tenure_delete, name='tenure_delete'),
    #-------------------------------------- PRODUCT N POLICY -------------------------------------------------
    path('add_prp',views.add_prp,name='add_prp'),
    path('master_product_policy', views.master_product_policy,name='Master Product Policy'),
    path('pp_edit/<int:id>', views.pp_edit, name='pp Edit'),
    path('pp_edit/pp_edit_table', views.pp_edit_table, name='Edit pp'),
    #------------------------------------------------ RESIDENCE -----------------------------------------------
    path('master_residence_type', views.master_residence_type,name='Master Residence Type'),
    path('residence_type_edit/<int:id>', views.residence_type_edit, name='residence type Edit'),
    path('residence_type_edit/residence_type_edit_table', views.residence_type_edit_table, name='Edit residence Type'),
    path('residence_type_delete/<int:id>', views.residence_type_delete, name='residence_type_delete'),
    #-------------------------------------- PRODUCT N POLICY ENTIRE MASTER -------------------------------------------------
    path('pp_master', views.pp_master, name='Entire PP Master'),
    #-------------------------------------- PRODUCT N POLICY ENTIRE MASTER SEARCH ---------------------------------------
    path('ppm_search/<int:id>', views.ppm_search, name='Search PPM'),
    #----------------------------------- CHECK ELIGIBILITY ---------------------------------------------------
    path('check_eligible/<int:id>', views.check_eligible, name='check eligibility'),

    path('cust_edit/<int:id>', views.cust_edit, name='cust_edit'),
    path('cust_view/<int:id>', views.cust_view, name='cust_view'),
    path('cust_edit/cust_edit_table', views.cust_edit_table, name='cust_edit_table'),
    #------------------------------------ DERIVED RESIDENCE-----------------------------------------------------------
    path('derived_residence', views.derived_residence,name='Derived Residence'),
    path('add_derived_residence', views.add_derived_residence,name='add_derived_residence'),
    path('add_derived_residence_table', views.add_derived_residence_table,name='add_derived_residence_table'),
    path('res_delete/<int:id>', views.res_delete, name='res_delete'),
    #------------------------------------ DERIVED SALARY-----------------------------------------------------------
    path('derived_salary', views.derived_salary,name='Derived salary'),
    path('add_derived_salary', views.add_derived_salary,name='add_derived_salary'),
    path('add_derived_salary_table', views.add_derived_salary_table,name='add_derived_salary_table'),
    path('sal_delete/<int:id>', views.sal_delete, name='sal_delete'),
    #------------------------------------ DERIVED company-----------------------------------------------------------
    path('derived_company', views.derived_company,name='Derived company'),
    path('add_derived_company', views.add_derived_company,name='add_derived_company'),
    path('add_derived_company_table', views.add_derived_company_table,name='add_derived_company_table'),
    path('com_delete/<int:id>', views.com_delete, name='com_delete'),
    #------------------------------------ DERIVED cocat-----------------------------------------------------------
    path('derived_cocat', views.derived_cocat,name='Derived cocat'),
    path('add_derived_cocat', views.add_derived_cocat,name='add_derived_cocat'),
    path('add_derived_cocat_table', views.add_derived_cocat_table,name='add_derived_cocat_table'),
    path('coc_delete/<int:id>', views.coc_delete, name='coc_delete'),
#------------------------------------ DERIVED tenure-----------------------------------------------------------
    path('derived_ten', views.derived_ten,name='Derived ten'),
    path('add_derived_ten', views.add_derived_ten,name='add_derived_ten'),
    path('add_derived_ten_table', views.add_derived_ten_table,name='add_derived_ten_table'),
    path('ten_delete/<int:id>', views.ten_delete, name='ten_delete'),
    #------------------------------------- REASONS -------------------------------------------------------------
    path('reasonsp', views.reasonsp, name='reasonsp'),
    path('add_rea', views.add_rea,name='add_rea'),
    path('add_rea_table', views.add_rea_table,name='add_rea_table'),
    path('rea_edit/<int:id>', views.rea_edit, name='rea_edit'),
    path('rea_edit/rea_edit_table', views.rea_edit_table, name='rea_edit_table'),
    path('rea_delete/<int:id>', views.rea_delete, name='rea_delete'),
#------------------------------------------------ FOIR -----------------------------------------------
    path('add_foir',views.add_foir,name='add_foir'),
    path('add_foir_table',views.add_foir_table,name='add_foir_table'),
    path('master_foir', views.master_foir,name='Master foir'),
    path('foir_edit/<int:id>', views.foir_edit, name='foir_edit'),
    path('foir_edit/foir_edit_table', views.foir_edit_table, name='Edit foir'),
    path('foir_delete/<int:id>', views.foir_delete, name='foir_delete'),

    path('login', views.login, name='login'),
    path('log', views.log, name='log'),
    path('cust_delete/<int:id>', views.cust_delete, name='cust_delete'),
    path('add_customer', views.add_customer,name='Add Customer Details'),
    path('add_customer_table', views.add_customer_table,name='Add Customer Details Table'),
    path('checks/<int:id>', views.checks, name='checks'),
    path('add_remark', views.add_remark,name='Add Remark'),
    path('rem_delete', views.rem_delete, name='rem_delete'),
    path('add_pro', views.add_pro,name='Add Processing Fee'),
    path('pro_delete', views.pro_delete, name='pro_delete'),
    path('master_comp_name', views.master_comp_name, name='master_comp_name'),
    path('add_comp_name', views.add_comp_name, name='add_comp_name'),
    path('add_comp_name_table', views.add_comp_name_table, name='add_comp_name_table'),
    path('comp_name_edit/<int:id>', views.comp_name_edit, name='comp_name_edit'),
    path('comp_name_edit/comp_name_edit_table', views.comp_name_edit_table, name='comp_name_edit_table'),
    path('loan_edit', views.loan_edit, name='loan_edit'),
    path('loan_edit_table', views.loan_edit_table, name='loan_edit_table'),
    path('credit_edit', views.credit_edit, name='credit_edit'),
    path('credit_edit_table', views.credit_edit_table, name='credit_edit_table'),
path('smail', views.smail, name='Mail Generation'),
    #path('mail', views.mail, name='Mail Generation'),
    path('whatsapp', views.whatsapp, name='WhatsApp Message Generation'),
    path('wMsg', views.wMsg, name='WhatsApp Message Generation'),
    path('gmail', views.gmail, name='Mail Message Generation'),
    path('gMsg', views.gMsg, name='Mail Message Generation'),
    path('csv', views.csv, name='Upload CSV'),
    path('done', views.done, name='Done'),
    path('ineff/<int:id>', views.ineff, name='Turn to Ineff'),
]

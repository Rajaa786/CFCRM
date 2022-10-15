from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import bank_cat


# Register your models here.
@admin.register(bank_cat)
class Imports(ImportExportModelAdmin):
    list_display = ('bank_name', 'co_name', 'cat', 'eff', 'ineff')

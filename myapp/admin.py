from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# from myapp.resources import ReportResource

class ReportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('bp_code', 'bp_name', 'district', 'profile', 'agreement_days', 'total_sales', 'contract_status','sales_month')

admin.site.register(Report, ReportAdmin)


class TargetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'total_targets', 'account_manager', 'sales_month')

admin.site.register(Target, TargetAdmin)
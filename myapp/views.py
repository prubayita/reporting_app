from django.shortcuts import render
from .models import *
from django.db.models import Count, Sum
from datetime import date
# from myapp.forms import FileUploadForm
from django.http import HttpResponse
from django.template import loader
import json
from decimal import Decimal


# Create your views here.
# def reports(request):
#   myreports = Report.objects.all().values()
#   template = loader.get_template('index.html')
#   context = {
#     'myreports': myreports,
#   }
#   return HttpResponse(template.render(context, request))

def login(request):
  template = loader.get_template('cred/login.html')
  return HttpResponse(template.render())




def table(request):
  mytable = Report.objects.all().values()
  template = loader.get_template('ui/table.html')
  context = {
    'mytable': mytable
  }
  return HttpResponse(template.render(context, request))

def graph_data_view(request):
    all_data = Report.objects.all().values()
     # Convert date objects to strings and Decimal objects to floats
    all_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in all_data
    ]

    data_json = json.dumps(list(all_data))
    return render(request, 'ui/test2.html', {'data_json': data_json})

def district_report_view(request):
    district_report = Report.objects.values('district').annotate(total_sales=Sum('total_sales'))
    return render(request, 'ui/test.html', {'district_report': district_report})


    # ... additional code for rendering the report ...

# def sector_report_view(request):
#     sector_report = Report.objects.values('sector').annotate(total_sales=Sum('total_sales'))
#     # ... additional code for rendering the report ...

# # ... additional view functions for other reports ...

# # Report based on district
# district_report = Report.objects.values('district').annotate(total_sales=Sum('total_sales'))

# # Report based on sector
# sector_report = Report.objects.values('sector').annotate(total_sales=Sum('total_sales'))

# # Report based on product
# product_report = Report.objects.values('product').annotate(total_sales=Sum('total_sales'))

# # Report based on sales month
# sales_month_report = Report.objects.values('sales_month').annotate(total_sales=Sum('total_sales'))

# # Report based on billing cycle
# billing_cycle_report = Report.objects.values('billing_cycle').annotate(total_sales=Sum('total_sales'))

# # Report based on end date
# end_date_report = Report.objects.values('end_date').filter(end_date__gte=date.today()).annotate(total_sales=Sum('total_sales'))

# # Report based on contract status
# contract_status_report = Report.objects.values('contract_status').annotate(total_sales=Sum('total_sales'))

# # Report based on account manager
# account_manager_report = Report.objects.values('account_manager').annotate(total_sales=Sum('total_sales'))


from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count, Sum
from datetime import date
# from myapp.forms import FileUploadForm
from django.http import HttpResponse
from django.template import loader
import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout

# Create your views here.
# def reports(request):
#   myreports = Report.objects.all().values()
#   template = loader.get_template('index.html')
#   context = {
#     'myreports': myreports,
#   }
#   return HttpResponse(template.render(context, request))

def login(request):
  if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('graph_data_view')  # Redirect to the desired page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
  return render(request, 'cred/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 


def table(request):
  mytable = Report.objects.all().values()
  template = loader.get_template('ui/table.html')
  context = {
    'mytable': mytable
  }
  return HttpResponse(template.render(context, request))

def graph_data_view(request):
    report_data = Report.objects.all().values()
     # Convert date objects to strings and Decimal objects to floats
    report_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in report_data
    ]

    # Fetch data from the Target model
    target_data = Target.objects.all().values()
    target_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in target_data
    ]

      # Convert QuerySet to list for JSON serialization
    target_data = json.dumps(list(target_data))
    report_data = json.dumps(list(report_data))
    
    # data_json = json.dumps(list(report_data))
    # return render(request, 'ui/test5.html', {'data_json': data_json})
    return render(request, 'ui/test2.html', {'report_data': report_data, 'target_data': target_data})


def monthly(request):
    report_data = Report.objects.all().values()
     # Convert date objects to strings and Decimal objects to floats
    report_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in report_data
    ]

    # Fetch data from the Target model
    target_data = Target.objects.all().values()
    target_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in target_data
    ]

      # Convert QuerySet to list for JSON serialization
    target_data = json.dumps(list(target_data))
    report_data = json.dumps(list(report_data))
    
    # data_json = json.dumps(list(report_data))
    # return render(request, 'ui/test5.html', {'data_json': data_json})
    return render(request, 'ui/monthly.html', {'report_data': report_data, 'target_data': target_data})

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


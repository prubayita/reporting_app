from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count, Sum
from datetime import date
# from myapp.forms import FileUploadForm
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render
from django.db.models import Sum, F
from .models import Report, Target
from django.http import JsonResponse
from collections import defaultdict

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
    target_data = Target.objects.all().values()

    # Convert date objects to strings and Decimal objects to floats
    report_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in report_data
    ]

    target_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in target_data
    ]

    # Extract unique account managers and products
    account_managers = list(set(item['account_manager'] for item in report_data))
    products = list(set(item['product'] for item in report_data))

    # Convert QuerySet to JSON
    target_data_json = json.dumps(list(target_data))
    report_data_json = json.dumps(list(report_data))

    return render(request, 'ui/test4.html', {
        'report_data': report_data_json,
        'target_data': target_data_json,
        'account_managers': account_managers,
        'products': products,
    })


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
    return render(request, 'ui/monthly5.html', {'report_data': report_data, 'target_data': target_data})

def district_report_view(request):
    district_report = Report.objects.values('district').annotate(total_sales=Sum('total_sales'))
    return render(request, 'ui/test.html', {'district_report': district_report})

def graph_data_view2(request):
    report_data = Report.objects.all().values()
    target_data = Target.objects.all().values()

    # Convert date objects to strings and Decimal objects to floats
    report_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in report_data
    ]

    target_data = [
        {key: value.strftime('%Y-%m-%d') if isinstance(value, date)
         else float(value) if isinstance(value, Decimal)
         else value for key, value in data.items()}
        for data in target_data
    ]

    # Extract unique account managers and products
    account_managers = list(set(item['account_manager'] for item in report_data))
    products = list(set(item['product'].strip() for item in report_data))  # Use strip() here

    # Convert QuerySet to JSON
    target_data_json = json.dumps(list(target_data))
    report_data_json = json.dumps(list(report_data))

    return render(request, 'ui/test2.html', {
        'report_data': report_data_json,
        'target_data': target_data_json,
        'account_managers': account_managers,
        'products': products,
    })




def monthly2(request):
    # Retrieve filter parameter (sales_month) from the GET request
    # selected_month  = request.GET.get('sales_month', '')

    # Filter the data based on the sales_month
  # Fetch data from the database and perform calculations
    # actuals = Report.objects.filter(sales_month=selected_month).aggregate(Sum('total_sales'))['total_sales__sum'] or Decimal(0)
    selected_month = 'January'
    # Filter records for the selected month
    # Filter records for the selected month
    actuals = Report.objects.filter(sales_month=selected_month)
    
    # Calculate the sum of 'total_sales' for each product
    product_actuals = actuals.values('product').annotate(total_actuals=Sum('total_sales'))
    
    # Get the target values from the Target model for the selected month
    # target_values = Target.objects.filter(sales_month=selected_month).values('product', 'total_targets')
    target_values = Target.objects.filter(sales_month=selected_month)
    product_target=target_values.values('product').annotate(total_targ=Sum('total_targets'))
    # Create a dictionary to store product-wise performance
    performance_data = {}
    
    # Calculate performance for each product
    for target in product_target:
        product = target['product']
        total_target = target['total_targ']
        
        # Look up the actuals for the product and order by 'total_actuals'
        actual = product_actuals.filter(product=product).order_by('-total_actuals').first()
        
        if actual:
            actual_sales = actual['total_actuals']
            performance = (actual_sales / total_target) * 100 if total_target != 0 else 0
        else:
            actual_sales = 0
            performance = 0
        
        performance_data[product] = {
            'actual_sales': actual_sales,
            'total_target': total_target,
            'performance': performance,
        }
    
    context = {
        'performance_data': performance_data,
        'selected_month': selected_month,
    }

    return render(request, 'ui/table.html', context)
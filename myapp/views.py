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
    return render(request, 'ui/monthly.html', {'report_data': report_data, 'target_data': target_data})

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


# def monthly2(request):
#     report_data = Report.objects.all().values()
#     target_data = Target.objects.all().values()
#     context= {
#         'report_data': report_data, 
#         'target_data': target_data
#         }
#     print(report_data)
#     return render(request, 'ui/monthly2.html', context)

# def monthly2(request):
   
#     report_data = Report.objects.values_list('product', flat=True).distinct()

#     # Convert the queryset to a set to eliminate duplicates
#     unique_products = set(report_data)

#     context = {
#         'unique_products': unique_products,
#     }
#     print(unique_products)    

#     return render(request, 'ui/monthly2.html', context)

def monthly2(request):
    report_data = Report.objects.all().values()
    # Retrieve filter parameter (sales_month) from the GET request
    sales_month = request.GET.get('sales_month', '')

    # Filter the data based on the sales_month
    # Create a dictionary to store aggregated data by account_manager and product
    summary_data = defaultdict(dict)

    # Calculate totals for each unique combination of account_manager and product in the report data
    for record in report_data:
        account_manager = record['account_manager']
        product = record['product']
        total_sales = record['total_sales']

        if account_manager not in summary_data:
            summary_data[account_manager] = {}

        if product not in summary_data[account_manager]:
            summary_data[account_manager][product] = 0

        summary_data[account_manager][product] += total_sales

    # report_data = Report.objects.filter(sales_month__iexact=sales_month).values()
    # target_data = Target.objects.filter(sales_month__iexact=sales_month).values()

    context = {
        'summary_data': summary_data,
        'sales_month': sales_month,
    }
    print(summary_data)
    
    return render(request, 'ui/table.html', context)



# def monthly2(request):
#     # Retrieve filter parameters from the GET request
#     sales_month = request.GET.get('sales_month', '')
#     product = request.GET.get('product', '')
#     account_manager = request.GET.get('account_manager', '')

#     # Build filters based on the provided parameters
#     report_filters = {}
#     target_filters = {}

#     if sales_month:
#         report_filters['sales_month__iexact'] = sales_month
#         target_filters['sales_month__iexact'] = sales_month

#     if product:
#         report_filters['product__iexact'] = product
#         target_filters['product__iexact'] = product

#     if account_manager:
#         report_filters['account_manager__iexact'] = account_manager
#         target_filters['account_manager__iexact'] = account_manager

#     # Query the database with the applied filters
#     report_data = Report.objects.filter(**report_filters).values()
#     target_data = Target.objects.filter(**target_filters).values()

#     context = {
#         'report_data': report_data,
#         'target_data': target_data,
#         'sales_month': sales_month,
#         'product': product,
#         'account_manager': account_manager,
#     }

#     return render(request, 'ui/table.html', context)
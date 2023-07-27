from django.urls import path
from . import views

urlpatterns = [
    path('', views.district_report_view, name='district_report_view'),
    path('t', views.graph_data_view, name='graph_data_view'),
    path('m', views.monthly, name='monthly'),
    path('table', views.table, name='table'),
    path('login', views.login, name='login')
]
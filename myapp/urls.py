from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('t', views.graph_data_view, name='graph_data_view'),
    path('t2', views.graph_data_view2, name='graph_data_view2'),
    path('m', views.monthly, name='monthly'),
    path('m2', views.monthly2, name='monthly2'),
    path('table', views.table, name='table'),
    path('login', views.login, name='login'),
    path('monthly-chart/', views.monthly_chart, name='monthly-chart'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('t', views.graph_data_view, name='graph_data_view'),
    path('m', views.monthly, name='monthly'),
    path('table', views.table, name='table'),
    path('login', views.login, name='login')
]
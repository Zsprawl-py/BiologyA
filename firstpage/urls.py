from django.urls import path
from . import views

# app_name = 'firstpage'

urlpatterns = [
    path('', views.first_page, name='firstpage')
    ]
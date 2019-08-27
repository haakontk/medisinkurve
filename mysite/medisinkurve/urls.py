from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manual/', views.manual, name='manual'),
    path('autofill/', views.autofill, name='autofill'),
    path('faq/', views.faq, name='faq'),
    path('om/', views.om, name='om'),
]

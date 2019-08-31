from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:sykehus>/metode/', views.metode, name='metode'),
    path('<str:sykehus>/autofill/', views.autofill, name='autofill'),
    path('<str:sykehus>/manual/', views.manual, name='manual'),
    path('faq/', views.faq, name='faq'),
    path('om/', views.om, name='om'),
]


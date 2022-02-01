from django.urls import path
from . import views

urlpatterns = [
    path('', views.cpf_display, name='cpf_display'),
    path('cpf_validate/', views.cpf_not_validate, name='cpf_not_validate'),
    path('cpf_validate/<str:cpf>', views.cpf_validate, name='cpf_validate'),
    path('catequisando/<str:cpf>', views.catequisando, name='catequisando'),
]
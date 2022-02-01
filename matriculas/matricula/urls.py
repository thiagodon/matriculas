from django.urls import path
from . import views

urlpatterns = [
    path('', views.cpf_display, name='cpf_display'),
    path('cpf_validate/', views.cpf_not_validate, name='cpf_not_validate'),
    path('cpf_validate/<str:cpf>', views.cpf_validate, name='cpf_validate'),
    path('catequisando/<str:cpf>', views.catequisando, name='catequisando'),
    path('proof_list/<str:cpf>', views.proof_list, name='proof_list'),
    path('proof/<str:cpf>', views.proof, name='proof'),
]